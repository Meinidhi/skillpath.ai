import os
import sys
import json
import csv

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.dirname(backend_dir))

from app.core.database import SessionLocal
from app.models.models import (
    User, LearnerProfile, Skill, LearnerSkill, CareerRole, CareerRequirement,
    LearningResource, LearningRoadmap, RoadmapVersion, RoadmapItem,
    Assessment, AssessmentQuestion, AssessmentAttempt, AgentExecution, MentorConversation
)

db_out_dir = r"D:\promptwars\PROJECT_DOCUMENTATION\evidence\database"
agent_out_dir = r"D:\promptwars\PROJECT_DOCUMENTATION\evidence\agents"

os.makedirs(db_out_dir, exist_ok=True)
os.makedirs(agent_out_dir, exist_ok=True)

db = SessionLocal()

def export_table(name, query, filename):
    records = []
    for r in query.all():
        d = {}
        for col in r.__table__.columns:
            val = getattr(r, col.name)
            # Sanitize password hashes and sensitive secrets
            if col.name == "hashed_password":
                val = "[REDACTED_PBKDF2_HASH]"
            elif hasattr(val, "isoformat"):
                val = val.isoformat()
            d[col.name] = val
        records.append(d)
        
    # Write JSON
    json_path = os.path.join(db_out_dir, f"{filename}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
        
    # Write CSV
    if records:
        csv_path = os.path.join(db_out_dir, f"{filename}.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows(records)
            
    print(f"Exported {len(records)} records for {name} -> {filename}.json/csv")
    return records

print("Exporting database tables...")
export_table("users", db.query(User), "users")
export_table("learner_profiles", db.query(LearnerProfile), "learner_profiles")
export_table("skills", db.query(Skill), "skills")
export_table("learner_skills", db.query(LearnerSkill), "learner_skills")
export_table("career_roles", db.query(CareerRole), "career_roles")
export_table("career_requirements", db.query(CareerRequirement), "career_requirements")
export_table("learning_resources", db.query(LearningResource), "learning_resources")
export_table("learning_roadmaps", db.query(LearningRoadmap), "learning_roadmaps")
export_table("roadmap_versions", db.query(RoadmapVersion), "roadmap_versions")
export_table("roadmap_items", db.query(RoadmapItem), "roadmap_items")
export_table("assessments", db.query(Assessment), "assessments")
export_table("assessment_questions", db.query(AssessmentQuestion), "assessment_questions")
export_table("assessment_attempts", db.query(AssessmentAttempt), "assessment_attempts")
export_table("mentor_conversations", db.query(MentorConversation), "mentor_conversations")

# Agent Executions -> into both database and agents evidence folders
agent_records = export_table("agent_executions", db.query(AgentExecution), "agent_executions")
agent_ledger_path = os.path.join(agent_out_dir, "agent_execution_ledger.json")
with open(agent_ledger_path, "w", encoding="utf-8") as f:
    json.dump(agent_records, f, indent=2)
print(f"Exported agent ledger ({len(agent_records)} entries) -> {agent_ledger_path}")

# Export Scenario A & Scenario B before/after evidence
demo_user = db.query(User).filter(User.email == "demo@skillpath.ai").first()
if demo_user:
    roadmaps = db.query(LearningRoadmap).filter(LearningRoadmap.user_id == demo_user.id).all()
    rm_evidence = []
    for r in roadmaps:
        v_list = []
        for v in r.versions:
            v_list.append({
                "version_number": v.version_number,
                "change_trigger": v.change_trigger,
                "change_reason": v.change_reason,
                "items_count": len(v.items),
                "created_at": v.created_at.isoformat() if v.created_at else None
            })
        rm_evidence.append({
            "roadmap_id": r.id,
            "career_id": r.career_id,
            "career_title": r.career.title if r.career else "Unknown",
            "is_active": r.is_active,
            "versions": v_list
        })
    with open(os.path.join(db_out_dir, "demo_user_roadmap_history.json"), "w", encoding="utf-8") as f:
        json.dump(rm_evidence, f, indent=2)
    print("Saved demo user roadmap version history evidence.")

db.close()
print("All evidence exports completed successfully.")
