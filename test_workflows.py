import sys
import os

# Ensure project root and backend are on sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(backend_dir)
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.core.database import SessionLocal, engine, Base
from app.core.init_db import init_db
from app.models.models import (
    User, LearnerProfile, CareerRole, Assessment, AssessmentAttempt,
    LearningRoadmap, RoadmapVersion, AgentExecution, LearningResource
)
from backend.agents.orchestrator import CustomOrchestrator

def run_tests():
    print("==================================================")
    print("   SKILLPATH AI - BACKEND WORKFLOW VERIFICATION   ")
    print("==================================================")

    # 1. Initialize DB & Seed Data
    print("\n[Step 1] Initializing SQLite Database & Seeding Data...")
    db = SessionLocal()
    init_db(db)
    print("✓ Tables created and verified.")
    careers_count = db.query(CareerRole).count()
    assessments_count = db.query(Assessment).count()
    resources_count = db.query(LearningResource).count()
    print(f"✓ Seeded {careers_count} career paths, {assessments_count} assessments, and {resources_count} learning resources.")

    # 2. Verify Demo User (Alex Chen)
    print("\n[Step 2] Verifying Demo User (Alex Chen)...")
    demo = db.query(User).filter(User.email == "demo@skillpath.ai").first()
    assert demo is not None, "Demo user must exist"
    
    # Ensure baseline profile starts targeted at Full Stack Developer (Career ID 1)
    profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == demo.id).first()
    fs_role = db.query(CareerRole).filter(CareerRole.title.like("%Full Stack%")).first()
    assert fs_role is not None
    if profile:
        profile.target_career_id = fs_role.id
        db.commit()
        db.refresh(profile)
    print(f"✓ Found Demo User: {demo.full_name} ({demo.email}), Target Career: {fs_role.title} (ID: {fs_role.id})")

    orchestrator = CustomOrchestrator(db)

    # 3. Test Full Stack Developer Initial Roadmap
    print("\n[Step 3] Generating Initial Roadmap for Full Stack Developer...")
    init_result = orchestrator.run_initial_onboarding_workflow(demo.id)
    assert init_result["status"] == "success"
    print(f"✓ Initial Workflow Completed:")
    print(f"  - Target Career: Full Stack Developer")
    print(f"  - Career Readiness: {init_result['readiness_score']}%")
    print(f"  - Initial Roadmap Version: {init_result['roadmap_version']}")
    print(f"  - Mentor Welcome: {init_result['mentor_welcome'][:100]}...")

    # 4. Verify Roadmap in DB
    roadmap = db.query(LearningRoadmap).filter(
        LearningRoadmap.user_id == demo.id,
        LearningRoadmap.is_active == True
    ).first()
    assert roadmap is not None
    assert len(roadmap.versions) >= 1
    v1 = roadmap.versions[-1]
    print(f"✓ Stored Roadmap Version {v1.version_number} with {len(v1.items)} modules.")

    # 5. Test Scenario B: Genuine 40% JavaScript Assessment Diagnostic Deficit
    print("\n[Step 4] Executing SCENARIO B: 40% JavaScript Assessment Submission...")
    js_assessment = db.query(Assessment).filter(Assessment.title.like("%JavaScript%")).first()
    assert js_assessment is not None, "JavaScript assessment required"

    # Exact 40.0% diagnostic test submission (2 correct out of 5 questions)
    score_40 = 40.0
    bad_attempt = AssessmentAttempt(
        user_id=demo.id,
        assessment_id=js_assessment.id,
        score=score_40,
        total_questions=5,
        correct_count=2,
        passed=False,
        weak_concepts=["Closures & Scope", "Async/Await & Error Handling"],
        answers_summary=[
            {"question_id": 1, "correct": True, "selected": "A"},
            {"question_id": 2, "correct": False, "selected": "C", "concept": "Closures & Scope"},
            {"question_id": 3, "correct": True, "selected": "B"},
            {"question_id": 4, "correct": False, "selected": "D", "concept": "Async/Await & Error Handling"},
            {"question_id": 5, "correct": False, "selected": "A", "concept": "Event Loop & Concurrency"}
        ]
    )
    db.add(bad_attempt)
    db.commit()
    db.refresh(bad_attempt)

    assess_result = orchestrator.run_assessment_workflow(demo.id, bad_attempt.id)
    assert assess_result["status"] == "success"
    assert assess_result["reassessment_needed"] is True, "Reassessment must be triggered for score < 65%"
    new_v = assess_result.get("new_roadmap_version") or assess_result.get("roadmap_version")
    assert new_v is not None, "A new roadmap version must be created for 40% deficit"

    print(f"✓ Scenario B Result:")
    print(f"  - Submitted Score: {assess_result['score']}% (2/5 correct)")
    print(f"  - Diagnostic Passed: False (Threshold: 65%)")
    print(f"  - Reassessment Needed: {assess_result['reassessment_needed']}")
    print(f"  - Resulting Adapted Roadmap Version: {new_v}")
    print(f"  - Linked Assessment Attempt ID {bad_attempt.id} -> Roadmap Version {new_v}")
    print(f"  - Mentor Feedback: {assess_result['mentor_feedback'][:120]}...")

    # Check that roadmap version contains remedial task
    db.refresh(roadmap)
    latest_v = roadmap.versions[0]
    has_remedial = any(item.status == "needs_revision" for item in latest_v.items)
    assert has_remedial, "Adapted roadmap must contain remedial practice task"
    print(f"✓ Adapted Roadmap Version {latest_v.version_number} contains remedial task ({has_remedial}).")

    # 6. Test Scenario A: Genuine Full Stack Developer -> AI Engineer Transition
    print("\n[Step 5] Executing SCENARIO A: Genuine Full Stack Developer -> AI Engineer Transition...")
    ai_career = db.query(CareerRole).filter(CareerRole.title == "AI Engineer").first()
    assert ai_career is not None, "AI Engineer career must exist"

    career_change_result = orchestrator.run_career_change_workflow(demo.id, ai_career.id)
    assert career_change_result["status"] == "success"
    assert career_change_result["from_career"] == "Full Stack Developer", f"Expected from_career 'Full Stack Developer', got '{career_change_result['from_career']}'"
    assert career_change_result["to_career"] == "AI Engineer", f"Expected to_career 'AI Engineer', got '{career_change_result['to_career']}'"
    assert career_change_result["from_career"] != career_change_result["to_career"], "Career change must be between two distinct careers"

    print(f"✓ Scenario A Result:")
    print(f"  - Transition Verified: '{career_change_result['from_career']}' -> '{career_change_result['to_career']}'")
    print(f"  - Recalculated Readiness: {career_change_result['new_readiness_score']}%")
    print(f"  - New Roadmap Version: {career_change_result['roadmap_version']}")
    print(f"  - Mentor Welcome: {career_change_result['mentor_welcome'][:120]}...")

    # 7. Verify All Roadmap Versions Remain Accessible
    print("\n[Step 6] Verifying Roadmap Version Preservation...")
    db.refresh(roadmap)
    print(f"✓ Total Stored Roadmap Versions for Alex Chen: {len(roadmap.versions)}")
    for v in roadmap.versions:
        print(f"  • Version {v.version_number}: Trigger='{v.change_trigger}', Reason='{v.change_reason[:60]}...' ({len(v.items)} items)")
    assert len(roadmap.versions) >= 3, "At least 3 roadmap versions must be preserved"

    # 8. Verify Execution Logs
    print("\n[Step 7] Verifying Agent Execution Logs...")
    logs = db.query(AgentExecution).filter(AgentExecution.user_id == demo.id).all()
    distinct_agents = set(l.agent_name for l in logs)
    print(f"✓ Found {len(logs)} execution records logged in database for Alex Chen.")
    print(f"✓ Distinct Agents Executed: {distinct_agents}")
    assert len(distinct_agents) == 6, f"All 6 agents must be executed, found {len(distinct_agents)}"

    db.close()
    print("\n==================================================")
    print("   ALL BACKEND ADAPTIVE TESTS PASSED SUCCESSFULLY! ")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
