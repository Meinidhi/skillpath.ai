# SkillPath AI — Intelligent Personalized Learning Platform

Developed for the **PromptWars X RTC** Competition.

SkillPath AI is an enterprise-grade educational technology SaaS platform that replaces one-size-fits-all curricula with autonomous multi-agent career architecture. The platform diagnoses learner abilities with empirical evidence, maps gaps against production market specifications, sequences personalized versioned roadmaps, and adapts in real time to performance deficits and changing career ambitions.

---

## 1. Architectural Highlights

- **100% Local Zero-Cost Execution**: Zero mandatory external AI APIs, zero OpenAI/Gemini/Claude keys required, zero paid hosting.
- **Six Specialized Python Agents**: Dedicated agent classes under `backend/agents/` orchestrated by a centralized `CustomOrchestrator` using a shared Pydantic `LearnerContext`.
- **Deterministic RuleBasedProvider**: Grounded, verifiable algorithms for skill calibration, career readiness scoring, prerequisite sequencing, and contextual mentor advice.
- **Relational Persistence**: SQLite zero-configuration database with SQLAlchemy 2.0 synchronous operations and automatic schema initialization.
- **Roadmap Versioning & History**: Preserves previous roadmaps when career goals change or diagnostics trigger reassessment (Version 1, Version 2, Version 3 all remain viewable).
- **Audit Ledger**: Comprehensive logging of agent execution times, input context summaries, output results, and status badges.
- **Modern Responsive SaaS UI**: React 18, TypeScript, Tailwind CSS, Lucide icons, and Recharts charts.

---

## 2. Six Specialized Agents

All agents are implemented as modular Python classes under `backend/agents/`:

| Agent | Responsibility | Core Logic |
| :--- | :--- | :--- |
| **Profile Agent** | Normalization & Context | Ingests education, declared skills, projects, and learning style into structured `LearnerContext`. |
| **Skill Analysis Agent** | Evidence Calibration | Weights self-declared skills (0.35 confidence) against empirical assessment scores (0.70–0.95 confidence). |
| **Career Agent** | Competency Matching | Calculates transparent Career Readiness Score: `Earned Weight / Total Required Weight`. |
| **Learning Agent** | Curriculum Sequencing | Organizes prerequisite competencies into structured roadmap modules with curated resources and practical mini-projects. |
| **Progress Agent** | Diagnostic Evaluation | Evaluates assessment outcomes, detects weak concept tags (<65%), and triggers adaptive remedial interventions. |
| **AI Mentor Agent** | Contextual Coaching | Provides grounded mentorship calibrated to real stored telemetry, roadmap milestones, and test diagnostics. |

---

## 3. Mandatory Adaptive Workflows

### Scenario A: Career Goal Transition
1. Learner begins with **Full Stack Developer** target (Readiness: ~29.4%, Version 1 Roadmap).
2. Learner switches target career to **AI Engineer**.
3. **Workflow Executed**:
   `Profile Agent` → `Skill Analysis Agent` → `Career Agent` → `Learning Agent` → `Save Version 3` → `AI Mentor Welcome`.
4. **Outcome**:
   - Readiness score recalculated against new mathematical specifications (~18.3%).
   - Identifies newly required competencies (Machine Learning, Deep Learning & PyTorch).
   - Generates Roadmap Version 3 while keeping Version 1 and 2 fully accessible.
   - AI Mentor welcomes learner to their new trajectory with grounded guidance.

### Scenario B: Poor Assessment Performance Adaptation
1. Learner takes **JavaScript Assessment** and scores poorly (**20% score**).
2. **Workflow Executed**:
   `Progress Agent` → `Skill Analysis Agent` → `Career Agent` → `Learning Agent` → `Save Version 2` → `AI Mentor Diagnostic Feedback`.
3. **Outcome**:
   - Progress Agent detects performance deficit (<65%) and isolates weak concepts (*Closures & Scope*, *Event Loop*, *Async/Await*).
   - Skill evidence updated with empirical deficit rating.
   - Roadmap Version 2 synthesized with high-priority **Remedial Practice Task** injected at the top.
   - AI Mentor delivers encouraging feedback detailing exact concepts to review.

---

## 4. Application Pages & Views

1. **Landing Page**: Value proposition, 6-agent overview, and 1-click Demo mode.
2. **Authentication Modal**: Registration, Login, and 1-click Competition Demo login (Alex Chen).
3. **Dashboard Command Center**: Career readiness gauge, active milestone card, upcoming pipeline, live agent telemetry.
4. **Learner Profile**: Academic degree, institution, experience tier, soft skills, projects, certifications.
5. **Skill Analysis Dashboard**: Proficiency distribution, evidence confidence meter, validated strengths vs growth areas, domain coverage bars.
6. **Career Trajectory Exploration**: Catalogue of 10 production roles with salaries, growth projections, and requirement tags.
7. **Career Matching & Comparison**: Deep-dive match report, mathematical formula transparency, and **1-Click Scenario A Demonstration Button**.
8. **Personalized Learning Roadmap**: Interactive milestone timeline, task status toggles, and **Roadmap Version Selector (v1, v2, v3)** with change reasons.
9. **Assessment Interface**: Diagnostic test engine with multiple choice questions, instant grading, explanations, and **1-Click Scenario B Demonstration Button**.
10. **Curated Resource Library**: Vetted free resources from MDN, freeCodeCamp, W3Schools, and official documentation platforms.
11. **Progress Analytics**: Recharts growth trajectory curves, competency radar distributions, and diagnostic history.
12. **AI Mentor Interface**: Contextual interactive chat with suggested quick prompt pills.
13. **Agent Activity Monitor**: Real-time status cards for all 6 agents and historical execution ledger table.
14. **Settings & Specifications**: Architecture specs, demo account reset, and FastAPI Swagger docs link.

---

## 5. Quick Startup Instructions (Windows 11)

### Option A: 1-Click Launch (Recommended)
Double-click `start_all.bat` in the project root:
```cmd
start_all.bat
```
This automatically launches both backend and frontend servers in separate command windows.

### Option B: Manual Startup

**Terminal 1 — Backend (FastAPI + SQLite)**:
```powershell
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
- API Root: http://127.0.0.1:8000
- Swagger Documentation: http://127.0.0.1:8000/docs

**Terminal 2 — Frontend (React + Vite)**:
```powershell
cd frontend
npm.cmd run dev
```
- Web Application: http://localhost:5173

---

## 6. Running Backend Workflow Tests

A standalone test script validates all adaptive scenarios and database persistence:
```powershell
python backend/test_workflows.py
```
**Verification results include**:
- Database initialization and seeding (10 careers, 4 assessments).
- Initial Full Stack Developer roadmap synthesis (Version 1).
- Poor assessment adaptive intervention & remedial task injection (Version 2).
- Career goal change to AI Engineer & curriculum reprioritization (Version 3).
- Retention of all roadmap versions.
- Distinct logging of all six agents in SQLite.

---

## 7. Demo Account Credentials

- **Email**: `demo@skillpath.ai`
- **Password**: `password123`
- Alternatively, click the green **"Enter Competition Demo Mode"** button on the navbar or login screen for instant 1-click access.
