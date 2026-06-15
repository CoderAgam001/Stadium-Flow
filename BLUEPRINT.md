# Technical Case Study: Systemic Architecture & Agentic Logic

**Prefer offline reading? [`Download the formatted PDF version here.`](Agentic_Logic_Blueprint.pdf)**

## TL;DR

* **The Build:** A real-time, agentic predictive queue rerouting system to solve physical stadium congestion.

* **The Constraint:** Core logic and MVP were architected in 3 hours during a live sprint. Full production deployment (security, UI theming, and cloud hosting) completed in 7 hours.

* **The Engine:** FastAPI (Backend), SQLite + Synthetic Data Simulator (Virtual Hardware), Streamlit (Frontend), and Gemini 2.5-Flash (Logic/Reasoning).

## 1. The Context: AI-Driven Orchestration

The way we build software has *fundamentally changed*.

Instead of writing every line of code step-by-step, developers now act like managers. You give the AI clear rules, context, and boundaries — and those instructions act as your new **"source code"** - **The System Prompt**.

While the AI handles the repetitive task of typing out the actual programming language, the human engineer is *still fully responsible* for the big picture: designing security, managing data flow, and ensuring the whole system actually works.

## 2. The Problem Statement

Large-scale physical venues experience extreme operational friction due to asymmetric crowd movement and localized capacity overloads during intervals.

Traditional logistical management relies on static signage or reactive manual intervention.
Stadium Flow solves this by introducing an autonomous, hardware-agnostic predictive routing framework.

## 3. System Overview & Architecture

Stadium Flow is an AI-driven predictive rerouting system designed to optimize crowd movement.

It operates as a continuous backend orchestrator, balancing incoming synthetic data with live AI-reasoned directives.

### Design Decisions & Tradeoffs

To achieve a functional MVP within a tight development window, the following architectural tradeoffs were made:

|Decision|Reason|
|-----|-----|
|`SQLite`|Fastest local persistence for rapid MVP development.|
|`Streamlit`|Rapid UI rendering for role-based dashboards without complex frontend code.|
|`Gemini 2.5-Flash`|Low latency, highly token-efficient cognitive layer.|
|`Synthetic Data`|No physical sensor access; enables immediate, hardware-agnostic testing.|
|`FastAPI`|Lightweight, high-performance API layer for backend orchestration.|

## 4. Deep Dive: Logic Flow & The Cognitive Layer

Rather than executing rigid, conditional pathfinding algorithms that fail during real-life crowd behavior, the system implements a **ReAct (Reason + Act)** cognitive architecture via the Gemini API.

### The End-to-End Execution Flow

1. `sim_engine.py` generates synthetic occupancy data.

2. `SQLite` stores the current stadium state.

3. `FastAPI` reads the live occupancy matrix.

4. Deterministic functions calculate exact distances, capacities, and trends.

5. `Gemini` receives the occupancy state, distance data, and routing context.

6. `Gemini` generates a contextual recommendation.

7. `FastAPI` returns a structured `JSON` response.

8. `Streamlit` displays live directives to the end-users.

```text
      [ Live Database State ]
                  │
                  ▼
  ┌───────────────────────────────┐
  │        1. Observation         │
  └───────────────────┬───────────┘
                  │ Contextual Ingestion
                  ▼
  ┌───────────────────────────────┐
  │        2. Reasoning           │
  └───────────────────┬───────────┘
                  │ Strategic Balancing
                  ▼
  ┌───────────────────────────────┐
  │          3. Action            │
  └───────────────────────────────┘
                  │
                  ▼
    [ UI Direction / Alert ]
```

### Under the Hood

This system runs in the background, constantly watching data without slowing down other tasks.

Here is how it works under the hood:

* **Observation**: The system constantly checks the database to track how many people are in every zone of the venue at any given moment.

* **Reasoning**: It looks for potential problems—like a crowd jam forming in one zone during a break — and calculates smart solutions, such as directing people to a less crowded ones1.

* **Action**: It sends clear, automatic instructions to screens or apps to guide people where to go.

### To Summarize

The system watches the crowd in real time, spots bottlenecks before they become an issue, and automatically updates the system states to keep people moving smoothly.

---

### The ReAct Python Logic

Here's the simplified python logic executing the described `ReAct` Architecture:

```python
@app.get("/get_recommendation/{user_zone_id}/{dest_zone_id}")
def get_recommendation(user_zone_id: int, dest_zone_id: int):
  # Compute exact math and fetch live states
  dist_to_dest = calculate_distance(user_x, user_y, dest_x, dest_y)
  stadium_context = fetch_zone_trends(all_zones)
  
  # Pass clean data as static context to Gemini
  ai_result = ai_service.get_structured_recommendation(user_zone, dest_zone, stadium_context, dist_to_dest)
  
  return {"directive": ai_result.recommendation, "distance": dist_to_dest}
```

You can find the actual logic inside *`backend/main.py`*.

## 5. The Hallucination Shield: AI vs. Deterministic Logic

Large Language Models are inherently probabilistic linguistic predictors, not precise compute engines. Unchecked, they introduce systemic vulnerability via data fabrication.

Stadium Flow enforces absolute data reliability by strictly separating cognitive reasoning from mathematical execution.

### AI Handles

✓ Recommendation generation

✓ Contextual reasoning and strategic balancing

✓ Generating human-readable directives

### AI Does Not Handle

✗ Distance calculations

✗ Occupancy tracking

✗ Database updates

✗ Capacity mathematics

✗ State persistence

By restricting the AI to **immutable parameters** and enforcing strict `JSON` schemas, the system drastically mitigates hallucination risks and prevents **prompt break-outs**.

---

### The Cognitive Routing Prompt

Here is the exact injection payload used in `backend/ai_service.py`:

```python
prompt = f"""
You are an AI Crowd Controller for a Cricket Stadium.

User is at: {user_zone['zone_name']}
User wants to go to: {dest_zone['zone_name']} 
(Current Occupancy: {dest_zone['current_occupancy']}/{dest_zone['capacity']}, Trend: {trends.get(dest_zone['zone_id'], 'stable')})
Direct Distance: {dist_to_dest} meters.

Stadium State:
{stadium_context}

TASK:
1. Analyze if the destination or the path to it is overcrowded.
2. Suggest the BEST route. If the destination is too full, suggest a nearby alternative or a specific route to avoid bottlenecks.
3. Provide clear, step-by-step navigation instructions.
"""
```

## 6. The Data Virtualization Layer (10s Ingestion Pulse)

To replicate a high-density internet-of-things (IoT) environment under rapid prototyping constraints, the physical infrastructure layer was completely virtualized.

A background simulation process (`sim_engine.py`) acts as a digital twin of the venue, executing randomized but statistically realistic crowd data every 10 seconds, while also updating the `SQLite` state engine.

* This structure allows for future-proof scaling.

* To deploy to production, the simulation engine is unplugged, and a live IoT sensor data pipeline is instead ingested directly into the API.

* The cognitive layer requires **zero code modifications** to transition from synthetic to live data.

## 7. Architectural Laws for Multi-Agent Systems

Through production stress-testing, the following engineering guidelines were established to guarantee system survival:

* **Avoid the *Terminal Trap*:** Never force the user to open multiple terminal windows just to run the system. Connect all background tasks to the main server so they start and stop automatically together.

* **Strict Separation of Concerns:** Keep reading and writing separate. The simulation engine only updates the database, while the user interface only reads from it.

* **Vague Prompt Mitigation:** If an agent gives a vague answer, the model isn't broken — it’s just starving for facts. Fix it by feeding precise data and clear rules directly into the prompt.

* **Graceful Failures:** Fallback mechanisms and execution layers must catch API dropouts or rate-limiting thresholds instantly, returning safe, structured error definitions to prevent application-wide crashes.

## 8. Appendix: The Master Prompt

Curious how the initial architecture was generated so quickly?

For details regarding the exact **Master Prompt (System Prompt)** used to architect the core backend logic and enforce the zero-bloat constraints during the 3-hour rapid-prototyping sprint, see the [`prompt.md`](prompt.md).
