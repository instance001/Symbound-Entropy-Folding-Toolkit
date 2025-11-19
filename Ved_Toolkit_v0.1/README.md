# VED Toolkit v0.1 – Vectorized Entropic Decomposition

**Project:** Symbound Entropy Architecture – Applied Toolkit  
**Authors:** Anthony + Instance001 Plus  
**License:** AGPL-3.0-or-later

---

## Overview

The VED Toolkit is a scientific, domain-agnostic implementation of **Vectorized Entropic Decomposition (VED)**.

It provides:

- A formal core model (`src/ved_core.py`)
- A VED-style diagnostic agent and a naïve baseline agent
- Simulation harness for comparing strategies under load
- Entropic and stability analysis utilities
- ASCII diagrams and practitioner worksheets
- Example scripts for running and inspecting experiments

This repository is the *applied* counterpart to the theoretical work in **Symbound-Entropy-Architecture**.

---

## Repository Structure

```text
docs/          – Formal documentation of the VED model
src/           – Python reference implementation
diagrams/      – ASCII diagrams (no binary dependencies)
worksheets/    – Field worksheets and checklists
examples/      – Example scripts and analysis notes
LICENSE        – AGPL-3.0-or-later notice
README.md      – This file
```

---

## Core Concepts (Short)

- Every task is a **demand vector** \(\vec{D}_i\)
- The system has a **capacity vector** \(\vec{C}\)
- A **routing cost** function \(R(i)\) decides feasibility and overhead
- Each task outcome is one of:
  - `RESOLVED`
  - `DEFERRED`
  - `COLLAPSED`
  - `TRANSFORMED`

From these, the toolkit computes:

- Resolution efficiency \(E_o\)
- Routing efficiency \(E_r\)
- Failure rate \(F\)
- Composite VED score \(S_{VED}\)

---

## Quick Start

### 1. Clone and enter the repo

```bash
git clone <your_repo_url_here>
cd VED_Toolkit_v0_1
```

### 2. Run the basic example

```bash
python examples/example_basic_run.py
```

This will:

- Generate a random task set
- Evaluate it under `VEDAgent` and `NaiveAgent`
- Print outcome counts and a VED score
- Render ASCII histograms of outcomes and routing costs

---

## Contents

### `docs/`

- `VED_Overview.md` – High-level introduction to VED
- `VED_Formal_Definitions.md` – Mathematical core of the model
- `VED_Field_Protocol.md` – Step-by-step procedure for running a VED study
- `VED_Domain_Mapping.md` – How VED maps to cognitive, AI, engineering, etc.
- `VED_Metrics_and_Scoring.md` – All metrics used in the toolkit
- `VED_Limitations_and_Assumptions.md` – Model boundaries and caveats

### `src/`

- `ved_core.py` – Capacity, tasks, routing cost, outcome logic, VED score
- `task_generator.py` – Deterministic and random task generation
- `ved_agent.py` – VED-style diagnostic agent
- `naive_agent.py` – Minimal baseline agent
- `ved_simulation.py` – Simulation harness for VED vs naive
- `analysis_tools.py` – Entropy, stability, and aggregation utilities
- `visualize.py` – ASCII-based visualizations

### `diagrams/ascii/`

Text-only diagrams describing:

- The VED pipeline
- Entropy routing
- Capacity vector space
- Outcome space
- Entropy folding
- VED vs naive comparison

### `worksheets/`

- `VED_Worksheet.md` – End-to-end experiment template
- `Domain_Capacity_Scan.md` – Capacity definition and normalization form
- `Expression_Pathways_Checklist.md` – Outcome and channel checklist
- `Resolution_Prediction_Form.md` – Pre-run prediction and post-run comparison

### `examples/`

- `example_basic_run.py` – Minimal runnable example
- `example_task_set.md` – Human-readable description of a test setup
- `example_analysis_notes.md` – Template for recording observations

---

## License

This project is released under the **GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later)**.

You are free to use, modify, and redistribute the toolkit under the terms of that license.  
For full details, see `LICENSE` in this repository and the FSF’s official text.

---
