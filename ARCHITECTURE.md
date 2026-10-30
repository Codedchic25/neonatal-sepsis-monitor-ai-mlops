# 🏗️ Sepsis Monitor AI – System Architecture & Engineering Documentation

---

## 📌 Executive Summary

The platform orchestrates real-time physiological telemetry monitoring with non-deterministic AI cognitive support through a layered, decoupled system topology. The software stack integrates:
- Streamlit Clinical Presentation Layer
- SQLAlchemy Object-Relational Mapper (ORM)
- Volatile and Core SQLite Database Engines
- Deterministic Clinical Rules Engine
- Isolated Post-Inference Guardrail Pipeline
- Promptfoo AI Safety and Validation Framework
- Multi-Stage GitHub Actions CI/CD Pipeline

---

## 🏗️ High-Level Architectural Layout

```text
┌────────────────────────────────────────────────────────┐
│               Streamlit Clinical UI                    │
└──────────────────────────┬─────────────────────────────┘
                           │ (Rerun Core Lifecycle Loop)
                           ▼
┌────────────────────────────────────────────────────────┐
│             Clinical Orchestration (app.py)            │
└──────────────────────────┬─────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
┌────────────────┐ ┌───────────────┐ ┌───────────────┐
│Telemetry Engine│ │  AI Service   │ │  Guardrails   │
└────────┬───────┘ └───────┬───────┘ └───────┬───────┘
         │                 │                 │
         ▼                 ▼                 ▼
┌────────────────┐ ┌───────────────┐ ┌───────────────┐
│   SQLite DB    │ │   Groq LLM    │ │Prompt Filters │
└────────┬───────┘ └───────────────┘ └───────────────┘
         │
         ▼
┌────────────────┐
│Alembic Migrat. │
└────────────────┘
```

---

## 📂 Repository Structure

```text
Sepsis-Monitor-AI/
├── app.py
├── export.py
├── promptfoo.yaml
├── pyproject.toml
├── uv.lock
├── ruff.toml
├── Dockerfile
├── assets/
│   └── audio/
├── src/
│   ├── config/
│   ├── database/
│   ├── guardrails/
│   ├── medical/
│   ├── notifications/
│   └── services/
└── tests/
    ├── test_clinical_auth.py
    └── test_system.py
```

---

## 🧠 Clinical Decision Engine Bounds

The application ingests nine discrete clinical vectors to map out real-time patient physiological statuses:
- **Cardiovascular / Respiratory Telemetry:** Heart Rate, Oxygen Saturation (SpO2), Blood Pressure.
- **Thermal Tracking:** Core Temperature.
- **Biomarker Kinetics:** C-Reactive Protein (CRP), Procalcitonin (PCT).
- **Biometric Profiles:** Infant Weight, Renal Function Status.
- **Non-Pharmacological Inventions (FCC):** Kangaroo Care state, Neuro-Musicotherapy loops.

---

## 🔬 Sepsis Risk Classification Logic

The system categorizes patient risk states using a hardcoded, deterministic threshold matrix:
- **HIGH-RISK STATE:** Triggered instantly if `PCT >= 0.5 ng/mL` OR `CRP >= 5.0 mg/L`. Worsening parameters route immediate alert strings directly to application backend system logs.
- **BIOCHEMICALLY STABLE STATE:** Maintained exclusively if `PCT < 0.5 ng/mL` AND `CRP < 5.0 mg/L`.

---

## 💊 Deterministic Medication Dosing Engine

To guarantee infant safety, all clinical calculations execute strictly outside the language model layers:
- **Ampicillin Protocol:** $100 \text{ mg/kg/day}$ split into precise 12-hour intravenous intervals ($50 \text{ mg/kg/injection}$).
- **Gentamicin Protocol:** $4 \text{ mg/kg/day}$ administered as a single, unified daily dose.

---

## 🛡️ Secure Perimeter & Guardrail Architecture

The framework deploys a robust, multi-layered defense model to prevent system exploits and boundary leaks:
1. **Cryptographic Gateway Verification:** Evaluates incoming access tokens against 64-character hexadecimal SHA-256 digests. Uses constant-time `hmac.compare_digest()` validation to completely neutralize side-channel timing analysis attacks.
2. **Deterministic Domination:** Micro-dosage limits are bound to immutable Python formulas, keeping the generative network completely isolated from medical calculations.
3. **Adversarial Pattern Filtration:** Untrusted textual payloads containing prompt injection triggers (such as `IGNORE`, `OVERRIDE`, `SYSTEM RESET`, `CLEAN`, `PRINT`, `REVEAL`) are automatically intercepted, logged, quarantined, and replaced with safe placeholder parameters before inference blocks are executed.
4. **Post-Inference Semantic Interception:** Generative outputs are bounded by rigid XML delimiters (`<RAPORT>`, `<MEDICATIE>`, `<FCC>`). The `NeonatalOutputGuardrail` class parses these blocks using regular expressions. If it catches a hallucinated value breaching the absolute neonatal ceiling (`>500mg`) or weight-relative bounds (`>150mg/kg`), it raises a `ClinicalGuardrailException`, halts UI rendering, and activates a safe fallback layout.

---

## 🗄️ Persistence Layer Engine

- **Dashboard Operations:** Employs optimized, raw SQL strings via Python's native, thread-safe `sqlite3` driver inside `app.py` to match the high-frequency rerunning lifecycle of Streamlit widgets with minimal rendering latency.
- **Architecture Portability:** Integrates a structured SQLAlchemy ORM coupled with an active Alembic versioning network to track schema schemas over time and ensure seamless portability to production-grade PostgreSQL engines.
