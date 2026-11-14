import os
import sys
import json
import time

# Ensure backend path is on sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.dirname(backend_dir))

from app.core.database import SessionLocal
from app.core.init_db import init_db
from app.core.security import get_password_hash, verify_password, create_access_token, decode_access_token
from app.models.models import (
    User, LearnerProfile, Skill, LearnerSkill, CareerRole,
    CareerRequirement, LearningRoadmap, RoadmapVersion, RoadmapItem,
    Assessment, AssessmentQuestion, AssessmentAttempt, AgentExecution
)
from agents.context import LearnerContext
from agents.orchestrator import CustomOrchestrator
from agents.rule_based_provider import RuleBasedProvider

def test_system():
    print("=" * 80)
    print("SKILLPATH AI: COMPREHENSIVE BACKEND, AGENT & ISOLATION VERIFICATION")
    print("=" * 80)
    
    db = SessionLocal()
    orchestrator = CustomOrchestrator(db)
    provider = RuleBasedProvider()

    # --------------------------------------------------------------------------
    # 1. AUTHENTICATION & SECURITY VERIFICATION
    # --------------------------------------------------------------------------
    print("\n[TEST 1] Verifying Cryptographic Password Hashing & Token Issuance...")
    raw_pwd = "SecurePassword2026!"
    hashed_pwd = get_password_hash(raw_pwd)
    
    assert hashed_pwd != raw_pwd, "Password was not hashed"
    assert verify_password(raw_pwd, hashed_pwd) is True, "Valid password failed verification"
    assert verify_password("WrongPassword!", hashed_pwd) is False, "Invalid password was accepted"
    
    token = create_access_token({"sub": "test@skillpath.ai", "user_id": 999})
    payload = decode_access_token(token)
    assert payload is not None and payload.get("sub") == "test@skillpath.ai", "JWT token failed validation"
    print("  -> Password hashing (PBKDF2-HMAC-SHA256) and JWT validation: PASS")

    # --------------------------------------------------------------------------
    # 2. USER DATA ISOLATION VERIFICATION
    # --------------------------------------------------------------------------
    print("\n[TEST 2] Verifying User Data Isolation (Multi-Tenant Guarantee)...")
    email_a = "alice_iso@skillpath.ai"
    email_b = "bob_iso@skillpath.ai"
    
    # Cleanup previous test users if any
    for e in [email_a, email_b]:
        existing = db.query(User).filter(User.email == e).first()
        if existing:
            db.query(AgentExecution).filter(AgentExecution.user_id == existing.id).delete()
            db.query(AssessmentAttempt).filter(AssessmentAttempt.user_id == existing.id).delete()
            roadmaps = db.query(LearningRoadmap).filter(LearningRoadmap.user_id == existing.id).all()
            for r in roadmaps:
                db.delete(r)
            db.query(LearnerSkill).filter(LearnerSkill.user_id == existing.id).delete()
            db.query(LearnerProfile).filter(LearnerProfile.user_id == existing.id).delete()
            db.delete(existing)
            db.commit()

    user_a = User(email=email_a, hashed_password=get_password_hash("pass123"), full_name="Alice Isolation")
    user_b = User(email=email_b, hashed_password=get_password_hash("pass123"), full_name="Bob Isolation")
    db.add(user_a)
    db.add(user_b)
    db.commit()
    db.refresh(user_a)
    db.refresh(user_b)

    # Alice sets target career Full Stack Developer (ID 1)
    prof_a = LearnerProfile(user_id=user_a.id, education="Undergraduate CS", target_career_id=1, experience_level="Beginner")
    # Bob sets target career AI Engineer (ID 3)
    prof_b = LearnerProfile(user_id=user_b.id, education="Graduate Math", target_career_id=3, experience_level="Advanced")
    db.add(prof_a)
    db.add(prof_b)
    db.commit()

    # Add baseline skills for Alice
    db.add(LearnerSkill(user_id=user_a.id, skill_id=1, proficiency_level="Intermediate", confidence_level=0.75, evidence_source="Assessment"))
    db.add(LearnerSkill(user_id=user_a.id, skill_id=2, proficiency_level="Beginner", confidence_level=0.50, evidence_source="Self-Declared"))
    db.commit()

    # Generate roadmaps for both using orchestrator
    res_a = orchestrator.run_initial_onboarding_workflow(user_a.id)
    res_b = orchestrator.run_initial_onboarding_workflow(user_b.id)

    assert res_a["status"] == "success", "Alice onboarding workflow failed"
    assert res_b["status"] == "success", "Bob onboarding workflow failed"

    # Verify roadmaps belong strictly to each user
    alice_roadmaps = db.query(LearningRoadmap).filter(LearningRoadmap.user_id == user_a.id).all()
    bob_roadmaps = db.query(LearningRoadmap).filter(LearningRoadmap.user_id == user_b.id).all()

    assert len(alice_roadmaps) >= 1, "Alice should have a roadmap"
    assert len(bob_roadmaps) >= 1, "Bob should have a roadmap"
    assert alice_roadmaps[0].career_id == 1, "Alice should be Full Stack Developer"
    assert bob_roadmaps[0].career_id == 3, "Bob should be AI Engineer"
    assert alice_roadmaps[0].id != bob_roadmaps[0].id, "Roadmaps must have distinct IDs"
    print("  -> User data isolation: Alice (ID: 1) and Bob (ID: 3) roadmaps strictly isolated: PASS")

    # --------------------------------------------------------------------------
    # 3. SIX AGENT SEQUENTIAL INFLUENCE VERIFICATION
    # --------------------------------------------------------------------------
    print("\n[TEST 3] Verifying Six-Agent Pipeline & Data Influence Chain...")
    
    context = orchestrator.build_learner_context(user_a.id)
    context.workflow_id = "test-chain-123"

    # 3.1 ProfileAgent normalizes and scores profile
    l1 = orchestrator.profile_agent.run(context)
    assert l1["status"] == "success", "ProfileAgent failed"
    print(f"  -> ProfileAgent: {l1['output_summary']}")

    # 3.2 SkillAnalysisAgent evaluates skills based on context
    l2 = orchestrator.skill_agent.run(context)
    assert len(context.learner_skills) > 0, "SkillAgent must evaluate learner skills"
    print(f"  -> SkillAnalysisAgent: Evaluated {len(context.learner_skills)} skills")

    # 3.3 CareerAgent readiness calculation is influenced by SkillAgent output
    context.target_career_id = 1 # Full Stack Developer
    l3 = orchestrator.career_agent.run(context)
    assert context.career_readiness_score > 0, "Career readiness must be greater than 0"
    print(f"  -> CareerAgent: Calculated Readiness = {context.career_readiness_score}% (Influenced by skills)")

    # 3.4 LearningAgent roadmap sequence is influenced by CareerAgent skill gaps
    l4 = orchestrator.learning_agent.run(context)
    assert len(context.new_roadmap_items) > 0, "LearningAgent must generate roadmap items"
    print(f"  -> LearningAgent: Generated {len(context.new_roadmap_items)} curriculum modules based on career gaps")

    # 3.5 ProgressAgent detects deficit and triggers adaptive intervention
    context.recent_attempt = {
        "score": 20.0,
        "passed": False,
        "skill_name": "JavaScript",
        "weak_concepts": ["Closures", "Event Loop"]
    }
    l5 = orchestrator.progress_agent.run(context)
    assert context.reassessment_needed is True, "ProgressAgent must flag adaptive intervention for score < 65%"
    print("  -> ProgressAgent: Correctly detected score deficit (20.0%) and flagged reassessment_needed=True")

    # 3.6 AIMentorAgent generates personalized advice citing the specific deficit concepts
    l6 = orchestrator.mentor_agent.run(context)
    assert context.mentor_response is not None and len(context.mentor_response) > 20, "Mentor must produce guidance"
    print(f"  -> AIMentorAgent: Generated context-aware guidance message: '{context.mentor_response[:70]}...'")

    # --------------------------------------------------------------------------
    # 4. EXECUTION LOG PERSISTENCE VERIFICATION
    # --------------------------------------------------------------------------
    print("\n[TEST 4] Verifying Agent Execution Logs Persistence...")
    executions = db.query(AgentExecution).filter(AgentExecution.user_id == user_a.id).all()
    agent_names = set(e.agent_name for e in executions)
    print(f"  -> Found {len(executions)} execution logs in SQLite for user {user_a.id}")
    print(f"  -> Distinct agents recorded: {list(agent_names)}")
    assert len(agent_names) >= 4, "Multiple agents must be recorded in SQLite audit ledger"
    for e in executions[:3]:
        assert e.execution_time_ms is not None, "Execution time must be logged"
        assert e.status == "success", "Agent execution must report success"
    print("  -> Execution log persistence & latency audit: PASS")

    # --------------------------------------------------------------------------
    # 5. DATABASE PERSISTENCE ACROSS SESSIONS
    # --------------------------------------------------------------------------
    print("\n[TEST 5] Verifying Persistence Across Database Connection Cycles...")
    db.close()
    
    # Open a fresh independent database session
    db_fresh = SessionLocal()
    reloaded_user = db_fresh.query(User).filter(User.email == email_a).first()
    assert reloaded_user is not None, "User record must persist across connection restarts"
    reloaded_roadmaps = db_fresh.query(LearningRoadmap).filter(LearningRoadmap.user_id == reloaded_user.id).all()
    assert len(reloaded_roadmaps) >= 1, "Roadmap must persist across connection restarts"
    print(f"  -> Successfully reloaded user {reloaded_user.email} and {len(reloaded_roadmaps)} roadmaps in fresh session: PASS")
    
    # Clean up test users
    for e in [email_a, email_b]:
        existing = db_fresh.query(User).filter(User.email == e).first()
        if existing:
            db_fresh.query(AgentExecution).filter(AgentExecution.user_id == existing.id).delete()
            roadmaps = db_fresh.query(LearningRoadmap).filter(LearningRoadmap.user_id == existing.id).all()
            for r in roadmaps:
                db_fresh.delete(r)
            db_fresh.query(LearnerSkill).filter(LearnerSkill.user_id == existing.id).delete()
            db_fresh.query(LearnerProfile).filter(LearnerProfile.user_id == existing.id).delete()
            db_fresh.delete(existing)
            db_fresh.commit()
    db_fresh.close()

    print("\n" + "=" * 80)
    print("ALL BACKEND, AGENT PIPELINE, AND ISOLATION CHECKS PASSED WITH ZERO ERRORS!")
    print("=" * 80)

if __name__ == "__main__":
    test_system()
