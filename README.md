# PURPLE — Round 2 Submission

## 1. Team Name

Purple Team 16 — **InfraPulse**

## 2. Problem Statement & Solution Description

**Problem Statement:**

City infrastructure services depend on one another. A power fault can spread to pumps, telecom towers and traffic signals, affecting hospital access and operations. Separate departmental views make it difficult to identify the next affected asset, the time available to act and the responsible response team.

**Proposed Solution:**

InfraPulse is a map-based infrastructure cascade simulator. Select an initial failure and explore how its effects propagate through infrastructure dependencies over time. A coordinated response center converts the simulation into department-specific priorities, action deadlines and a downloadable briefing. The prototype includes a synthetic Bengaluru network of 33 assets and 66 dependencies. Dependencies and backup durations are assumed for demonstration.

## 3. Selected Features

### Feature 1: Dependency Cascade Simulation and Timeline

A Python/FastAPI backend models infrastructure as a directed dependency graph. Its deterministic engine accounts for backup durations, redundant supply groups and downstream failures. A React/TypeScript frontend displays the returned results on an interactive map with dependency arcs, status markers and a scrub/play timeline. Preset scenarios and custom trigger selections are supported in LIVE mode.

### Feature 2: Coordinated Department Response Center

The response center shows current asset statuses, department impact and hospital watch information. Prioritized actions are grouped into Act now, Next 30 min and Later, with simulation-time deadlines, asset location controls, department filters and a situation briefing. A dispatch checklist records local UI readiness only; it does not change the simulation.

## 4. Setup & Running Instructions

Requirements: Node.js 20+ with npm, and Python 3.11+. Internet is required for basemap tiles. Fonts are self-hosted.

Clone this repository:

```bash
git clone https://github.com/Tech-Forge74/purple_team_16.git
cd purple_team_16
```

Start the backend in terminal 1:

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

On Windows, activate with `.venv\Scripts\activate` and use the installed Python 3.11+ command.

Start the frontend in terminal 2:

```bash
cd frontend
npm ci
```

Create `frontend/.env.local` with:

```dotenv
VITE_USE_MOCK=false
VITE_API_BASE=http://127.0.0.1:8000
```

Then run:

```bash
npm run dev -- --port 5173
```

Open http://localhost:5173 and confirm the LIVE badge. Backend API documentation is at http://127.0.0.1:8000/docs. To use the recorded fallback, set `VITE_USE_MOCK=true` and restart Vite. Mock mode has a separate 14-asset dataset and supports its three recorded presets.

Validation:

```bash
# frontend
npm test
npm run build
npm run test:live  # backend must be running; POSIX shell

# backend, activated virtual environment
python -m pytest -q
```

The frontend build, 20 default frontend tests, the live HTTP integration test and 16 backend tests passed during project verification.

## 5. Feature Demonstration

### Feature 1: Dependency Cascade Simulation and Timeline

1. Open the app and skip the intro or choose Explore the cascade. Select **Local substation trip**; selecting a preset runs it automatically. Run simulation reruns the selected triggers.
2. Restart the timeline at T+0. The Marathahalli substation and its immediate unbuffered dependency are down, while buffered dependencies show At risk.
3. Scrub to T+25 minutes. The result shows an impact on Rainbow Children's Hospital access roads through traffic-signal dependencies; this is a modeled service/access impact.
4. Continue through T+120 and T+150 to inspect tower battery exhaustion, or press Play. Statuses and counters update without another simulation request.
5. Try **Transmission station failure** and **Storm - two substations** to compare wider cascades. In LIVE mode, click a map asset, choose Fail this node and run a custom trigger combination.

**Expected outcome:** the map, dependency progress, chart, event feed and counters consistently reflect the returned failure times and current slider time.

### Feature 2: Coordinated Department Response Center

1. Open the Response center drawer on tablet/mobile; it is visible on desktop.
2. Inspect live Down/At risk counts, department bars and hospital countdowns. Scroll to Response actions and filter by department.
3. Advance the timeline. Action deadlines decrease and cards move between urgency lanes. Choose Locate asset to focus the corresponding map node.
4. Toggle a Dispatched checkbox. The local readiness indicator updates; simulation statuses remain unchanged.
5. Open Situation briefing to copy the summary or choose Download briefing to save it.

**Expected outcome:** each department receives a prioritized action list with time-sensitive context, asset location and a shareable briefing.

For a guided walkthrough, use **Auto-demo** for the approximately 66-second presenter tour. Shortcuts: Space play/pause, arrows step five minutes, P presenter mode, F follow, ? help and Esc exit.

See [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) for architecture, contract synchronization, test details and remaining polish limits. The original repository submission template is retained in [SUBMISSION_TEMPLATE.md](SUBMISSION_TEMPLATE.md).
