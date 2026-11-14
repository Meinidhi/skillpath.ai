# SkillPath AI: Competition Presentation & Demo Walkthrough Guide

**Project:** SkillPath AI — Autonomous Multi-Agent Personalized Learning Platform  
**Target Competition:** PromptWars X RTC  
**Target Role for Demo:** Alex Chen (`demo@skillpath.ai` / password: `password123`)  
**Architecture:** 100% Local (FastAPI + SQLite + React 18 + TypeScript + Vite + 6 Python Agents)  
**Zero Paid Dependencies:** No OpenAI, Claude, or Gemini API keys required. No heavy local LLM dependencies.

---

## 1. The Core Problem & Our Value Proposition (30-Second Elevator Pitch)

> *"Traditional online learning platforms offer the exact same static syllabus to every student regardless of what they already know, how they perform, or where they want their career to go.*  
>  
> *SkillPath AI solves this through a local, deterministic multi-agent architecture. Six specialized Python agents collaborate via a central orchestrator to evaluate real skill evidence, benchmark readiness against live industry job specifications, generate personalized roadmaps, and dynamically adapt when the student changes their career goals or struggles on diagnostic tests."*

---

## 2. 5-Minute Live Judge Demonstration Script

Follow these exact steps during the live demo:

### Step 1: Launch & Landing Page (30s)
1. Double click `start_all.bat` (or run `http://localhost:5173`).
2. Show the **Hero Section**: Highlight the problem statement, zero-cost guarantee, and the cards for all **6 Specialized Python Agents**.
3. Click the blue button: **"Explore Demo as Alex Chen"** (instant 1-click authentication).

### Step 2: Learning Command Center Dashboard (45s)
1. Point to the **Career Readiness Gauge**: Alex starts at **29.4%** (or current score) towards **Full Stack Developer**.
2. Explain the **Active Milestone Card**: Highlights current priority task with estimated duration and practical hands-on exercise.
3. Show the **Agent Activity Ticker**: Real-time ticker showing the latest autonomous actions taken by the 6 agents.

### Step 3: Skill Evidence Calibration & Transparent Scoring (1m)
1. Click **"Skill Analysis"** in top navbar:
   - Show how self-declared skills carry lower confidence (~0.35), while empirical diagnostic test results boost confidence to 0.75–0.95.
2. Click **"Career Match"** in top navbar:
   - Highlight the **Transparent Mathematical Formula**:
     $$\text{Readiness Score} = \left( \frac{\text{Earned Weighted Competency}}{\text{Total Required Competency}} \right) \times 100$$
   - Show the breakdown of **Skills Meeting Requirements**, **Underdeveloped Skills**, and **Critical Missing Skills**.

### Step 4: The Core Differentiator — Adaptive Workflow Demonstrations (2m)

#### 🚀 Demonstration A: Scenario B (Diagnostic Test Deficit Adaptation)
1. Click **"Assessments"** in top navbar.
2. Point out the **JavaScript Assessment** card.
3. Click the orange button: **"Execute Scenario B (20% Diagnostic Score)"**.
4. **Observe the immediate adaptation**:
   - The test evaluates 1/5 correct (20% score).
   - **Progress Agent** flags concept deficits in *Closures & Scope* and *Event Loop*.
   - **Learning Agent** automatically generates **Roadmap Version 2**, injecting targeted remedial practice tasks before advanced topics.
   - **AI Mentor** emits tailored coaching on closures and asynchronous JavaScript.
5. Click **"Roadmap"** in navbar: Toggle between **Version 1** and **Version 2** in the version dropdown to prove version history preservation!

#### 🎯 Demonstration B: Scenario A (Career Goal Transition)
1. Click **"Career Match"** in navbar.
2. Click the purple button: **"Execute Scenario A (Switch to AI Engineer)"**.
3. **Observe the multi-agent cascade**:
   - Target career switches to **AI Engineer**.
   - **Career Agent** recalculates readiness down to **18.3%** (highlighting missing Deep Learning & PyTorch skills).
   - **Learning Agent** synthesizes **Roadmap Version 3** with AI/ML curricula while **preserving Versions 1 and 2**.
   - **AI Mentor** sends a warm domain-switch welcome message.
4. Go to **"Roadmap"**: Open the version selector to show all 3 versions preserved and accessible!

### Step 5: Multi-Agent Activity Ledger (45s)
1. Click **"Agent Activity"** in navbar.
2. Show the **6 Agent Status Cards**: Profile Agent, Skill Analysis Agent, Career Agent, Learning Agent, Progress Agent, AI Mentor Agent.
3. Scroll through the **Execution Audit Ledger Table**:
   - Show exact execution timestamps, latency in milliseconds, input summaries, and output summaries recorded in SQLite.
   - Emphasize to the judges: *"This is verifiable agent orchestration, not hardcoded mock UI cards."*

---

## 3. Anticipated Judge Questions & Bulletproof Answers

**Q1: How do the agents operate without an external LLM API?**  
> *"We implemented a deterministic intelligence layer using our `RuleBasedProvider` and specialized Python classes. The agents execute real weighted mathematical formulas, set operations for gap identification, directed acyclic dependency sequencing for curriculum modules, and contextual templating grounded in stored SQLite state. This guarantees zero latency, zero cloud costs, and 100% deterministic reliability."*

**Q2: How does data flow between the agents?**  
> *"Every agent operates over a shared Pydantic `LearnerContext`. The output of the Profile Agent informs the Skill Analysis Agent; the calibrated skills feed into the Career Agent's readiness algorithm; the identified career gaps determine the Learning Agent's roadmap items; and diagnostic test outcomes trigger the Progress Agent to inject remedial modules into the roadmap."*

**Q3: Can an external LLM be plugged in later?**  
> *"Yes. The architecture uses clean abstraction boundaries. The `RuleBasedProvider` interface can be swapped for an `OpenAIProvider`, `GeminiProvider`, or local Ollama client simply by implementing the provider interface without changing the database schema or agent orchestrator."*

---

## 4. Quick Verification Commands

- Backend Workflow Tests: `python backend/test_workflows.py`
- Multi-Tenant & Isolation Tests: `python backend/verify_full_system.py`
- Frontend Production Build: `cd frontend && npm run build`
- Launch Application: `start_all.bat`
