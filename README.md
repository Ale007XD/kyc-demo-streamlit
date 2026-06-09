# kyc-demo-streamlit

**Governance layer demo built on top of a KYC pipeline.**

This is not a KYC product. This is a demonstration of execution governance over an AI-driven compliance pipeline.

---

## What this is not

- Not OCR
- Not identity verification
- Not liveness detection
- Not sanctions screening
- Not a competitor to Jumio, Onfido, or Comply Advantage

Those systems sit *below* nano-vm in the stack. This demo governs them — it does not replace them.

---

## What this is

An interactive visualization of how a governance runtime behaves when placed above an AI pipeline.

The demo simulates six KYC pipeline steps, then shows what happens to execution traces, receipts, and audit artifacts when the governance layer is intact — and when it's deliberately broken.

```
OCR / Liveness / Screening providers
              ↓
   nano-vm Governance Layer       ← this demo
              ↓
   Human / Compliance Decision
```

The governance layer controls:

- which steps can execute
- in what order
- with what outputs
- under what policy constraints
- producing what verifiable artifacts

It does not perform identity verification. It governs the execution of the pipeline that does.

---

## Why this matters

Most AI demos optimize for accuracy.

This demo optimizes for auditability.

Every decision produces an execution trace.  
Every trace produces a deterministic receipt.  
Every receipt is a recomputable projection of the trace — independent of the model.

```
Receipt = f(Trace)
```

This is the property that makes governed AI execution auditable: the receipt can be verified without re-running the model.

---

## Stack position

```
Data / Document Layer
        ↓
OCR / Screening / Liveness
  (Jumio · Onfido · Comply Advantage)
        ↓
nano-vm Execution Governance Layer   ← what this demo shows
        ↓
Execution Trace + Receipt
        ↓
Human Review / Compliance Decision
```

nano-vm sits between the AI pipeline and the compliance decision. It controls *what the agent does* — not what data it sees (that's Archestra, a complementary layer).

---

## Pipeline

The demo executes a six-step KYC review pipeline under FSM governance:

```
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

Each step has explicit transition constraints. The model cannot reorder, skip, or override them.

---

## Execution artifacts

Every run produces:

| Artifact | Description |
| :--- | :--- |
| **Trace** | Step-by-step execution record with SHA-256 Merkle chain |
| **TraceHealthReport** | Rollback density, tool churn rate, path variance, transition entropy |
| **ExecutionReceipt** | Minimal decision state — `Receipt = f(Trace)` |
| **NarrativeReceipt** | Human-readable summary for compliance review |

---

## Fault injection

Seven adversarial injectors demonstrate how the governance layer responds to corruption and attack:

| Injector | What it simulates |
| :--- | :--- |
| `invalid_program` | Malformed program structure before execution |
| `skip_step` | Attempt to bypass a required step |
| `reorder_steps` | Steps submitted out of governance order |
| `tool_injection` | Unauthorized tool call injected into pipeline |
| `policy_bypass` | Attempt to execute without policy constraints |
| `corrupt_receipt` | Receipt tampered after generation |
| `gdpr_erase` | Tombstoning event mid-pipeline |

The injectors make visible what silent failure looks like — and why deterministic enforcement matters.

---

## Built with the agent it governs

Part of this codebase was written by `nano-vm-dev-agent` — the same governed execution runtime that the demo visualizes.

The agent operates under the same governance model as the KYC pipeline:

```
Patch Proposal
      ↓
validate_staged_mypy()    ← tmpdir gate, disk untouched
      ↓
commit_patches()          ← atomic write on mypy pass
      ↓
run_pytest()              ← structural gate
      ↓
ExecutionReceipt          ← verifiable outcome
```

Every code change went through the same receipt-producing execution pipeline the demo shows. The governance model is not a demo artifact — it's the development environment.

---

## Stack

- Python 3.10+
- Streamlit 1.35+
- llm-nano-vm
- nano-vm-mcp
- Pydantic v2
- pytest
- mypy --strict
- Ruff

---

## Architecture

```
app.py
│
├── components/
│   ├── comparison_panel.py     ← naïve vs governed execution
│   ├── governance_stream.py    ← real-time governance events
│   ├── policy_lock.py          ← immutable checkpoints
│   ├── trace_health.py         ← runtime health metrics
│   ├── entropy_panel.py        ← transition entropy visualization
│   ├── injector_panel.py       ← adversarial fault injection
│   ├── narrative_receipt.py    ← human-readable receipt
│   └── audit_panel.py          ← audit metadata
│
├── engine/
│   ├── mock_runtime.py         ← simulated FSM execution
│   ├── program_validator.py    ← pre-flight static analysis
│   └── trace_analyzer.py       ← post-hoc trace interpretation
│
├── store/
│   ├── execution_state.py      ← session state management
│   └── injector_state.py       ← injector configuration
│
└── tests/                      ← 51 tests, mypy --strict
```

---

## Installation

```bash
git clone https://github.com/Ale007XD/kyc-demo-streamlit.git
cd kyc-demo-streamlit
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Run

```bash
streamlit run app.py
```

Default: `http://localhost:8501`

---

## Testing

```bash
pytest -q        # 51 passed
mypy .           # Success: no issues found
```

---

## Design principles

**Trace as source of truth.** Receipts and analysis are projections. The trace is authoritative.

**Post-hoc analysis only.** `TraceAnalyzer` never mutates runtime state. `Receipt = f(Trace)` is computed after the fact, not during execution.

**Failure as first-class outcome.** `FAILED`, `POLICY_BLOCKED`, `INSUFFICIENT_DATA` are legitimate terminal states, not exceptions to be swallowed. The demo surfaces them intentionally.

**Governance is structural.** Evaluator blindness, policy enforcement, and transition constraints are properties of the runtime — not configurations, not prompts.

---

## Related projects

| Project | Role |
| :--- | :--- |
| [llm-nano-vm](https://github.com/Ale007XD/nano_vm) | Execution governance runtime — core library |
| [nano-vm-mcp](https://github.com/Ale007XD/nano-vm-mcp) | MCP gateway with GovernanceEnvelope and SQLite WAL |
| nano-vm-dev-agent | Governed development agent — wrote part of this codebase |

---

## Status

```
sprint_kyc_demo: COMPLETE
12 iterations · 51/51 pytest PASS · mypy strict PASS
```

---

## License

MIT
