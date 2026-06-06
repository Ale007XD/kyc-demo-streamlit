# kyc-demo-streamlit

Governance-first KYC demo built on top of the nano-vm ecosystem.

Interactive Streamlit SPA demonstrating:

* deterministic FSM execution for LLM pipelines
* governance-aware orchestration
* execution trace analysis
* entropy / instability detection
* policy locks and auditability
* adversarial fault injection
* replayable execution semantics

---

# Overview

`kyc-demo-streamlit` is a public demo application for the nano-vm ecosystem:

* `llm-nano-vm`
* `nano-vm-mcp`
* `nano-vm-dev-agent`

The demo simulates a KYC / AML review pipeline and visualizes how governance and deterministic orchestration differ from naïve agent execution.

The application is intentionally designed as:

* governance-first
* replay-oriented
* audit-oriented
* traceable
* failure-visible

This is not a chatbot UI.

This is an execution-governance visualization system.

---

# Core Concepts

## Deterministic FSM Runtime

The pipeline executes as a deterministic finite-state machine instead of unconstrained autonomous agent loops.

Each step has explicit transitions and governance constraints.

Example pipeline:

```text
collect_customer_data
    ↓
screen_sanctions
    ↓
adverse_media_search
    ↓
agent_review
    ↓
human_approval
    ↓
governance_seal
```

---

## Governance Layer

The demo visualizes:

* policy enforcement
* execution boundaries
* capability restrictions
* trace projection
* deterministic execution flow
* operator checkpoints

---

## Trace Analysis

The runtime generates execution traces that are analyzed post-hoc.

Metrics include:

* rollback density
* tool churn rate
* path variance
* transition entropy
* invariant violations

The analyzer is intentionally implemented as:

```text
Trace → Analyzer → Receipt
```

NOT:

```text
Runtime → mutable hidden state
```

---

## Fault Injection

The demo includes adversarial injectors to simulate runtime corruption and governance failures.

Available injectors:

* invalid_program
* skip_step
* reorder_steps
* tool_injection
* policy_bypass
* corrupt_receipt
* gdpr_erase

These demonstrate how deterministic governance systems behave under failure and attack conditions.

---

# Stack

* Python 3.10+
* Streamlit 1.35+
* llm-nano-vm
* nano-vm-mcp
* Pydantic v2
* pytest
* mypy --strict
* Ruff

---

# Architecture

```text
app.py
│
├── components/
│   ├── comparison_panel.py
│   ├── governance_stream.py
│   ├── policy_lock.py
│   ├── trace_health.py
│   ├── entropy_panel.py
│   ├── injector_panel.py
│   ├── narrative_receipt.py
│   └── audit_panel.py
│
├── engine/
│   ├── mock_runtime.py
│   ├── program_validator.py
│   └── trace_analyzer.py
│
├── store/
│   ├── execution_state.py
│   └── injector_state.py
│
└── tests/
```

---

# Installation

## Clone repository

```bash
git clone https://github.com/Ale007XD/kyc-demo-streamlit.git
cd kyc-demo-streamlit
```

---

## Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# Run Application

```bash
streamlit run app.py
```

Default URL:

```text
http://localhost:8501
```

---

# Testing

## Run pytest

```bash
pytest -q
```

Expected:

```text
51 passed
```

---

## Run mypy

```bash
mypy .
```

Expected:

```text
Success: no issues found
```

---

# Demo Features

## Comparison Panel

Compares:

* naïve agent execution
* governed deterministic execution

---

## Pre-flight Validation

Validates program structure before execution:

* missing targets
* unreachable nodes
* invalid transitions
* execution integrity

---

## Governance Stream

Real-time visualization of governance events and execution flow.

---

## Policy Lock

Shows immutable governance checkpoints and execution sealing.

---

## Trace Health

Displays runtime health metrics and execution anomalies.

---

## Entropy Panel

Visualizes transition entropy and instability indicators.

High entropy may indicate:

* nondeterministic branching
* unstable orchestration
* semantic drift
* probabilistic execution collapse

---

## Narrative Receipt

Human-readable execution receipt generated from deterministic trace data.

---

## Audit Panel

Displays audit-oriented execution metadata and governance artifacts.

---

# Design Principles

## Governance-first

Governance is part of runtime semantics — not an external observer.

---

## Trace as Source of Truth

Execution traces are authoritative.

Receipts and analysis are projections.

---

## Post-hoc Analysis

The analyzer does not mutate runtime state.

```text
TraceAnalyzer = pure post-processing layer
```

---

## Explicit Failure Visibility

Failures are surfaced intentionally.

The system avoids hidden retries and silent correction.

---

# Constraints

Important runtime constraints:

* NO eval()/exec()
* AST-based condition engine only
* deterministic step transitions
* terminal states explicitly marked
* no hidden autonomous loops
* no method calls in DSL conditions

---

# Current Status

```text
sprint_kyc_demo: COMPLETE
```

Results:

* 12 iterations
* 51/51 pytest PASS
* mypy strict PASS
* governance-first SPA complete

---

# Related Projects

## llm-nano-vm

Deterministic FSM runtime for LLM pipelines.

## nano-vm-mcp

MCP gateway and orchestration layer for nano-vm.

## nano-vm-dev-agent

Governed development agent with transactional patching.

---

# Roadmap

Planned next steps:

* ExecutionReceipt infrastructure
* OpenTelemetry spans
* per-model divergence metrics
* vm.step() incremental execution
* governed circuit breaker
* semantic drift analysis

---

# Philosophy

Most agent systems optimize for autonomy.

nano-vm optimizes for:

* determinism
* governance
* replayability
* auditability
* constrained execution semantics

The objective is not “more autonomous agents”.

The objective is reliable execution infrastructure for probabilistic models.

---

# License

MIT
