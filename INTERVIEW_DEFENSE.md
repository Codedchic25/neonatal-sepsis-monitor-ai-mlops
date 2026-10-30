# 🩺 Sepsis Monitor AI – Interview Defense Manual

## Section 1 – Project Overview

### 1. Tell me about your project?
**Answer:**
Sepsis Monitor AI is a neonatal Clinical Decision Support System (CDSS) prototype designed to assist healthcare professionals by centralizing real-time vital parameters, inflammatory biomarkers, weight-based medication calculations, and Family-Centered Care (FCC) metrics. The platform combines a responsive Python user interface, secure cryptographic role verification, deterministic medical rule layers, and an automated MLOps AI safety evaluation matrix.

### 2. Why did you build this project?
**Answer:**
I wanted to combine my professional clinical background in neonatology with my transition into software engineering and applied artificial intelligence. This project allowed me to solve a high-acuity healthcare problem while demonstrating hands-on mastery over production-grade engineering practices: strict type safety, cryptographic security, deterministic guardrails, automated testing, and CI/CD pipelines.

### 3. What problem does the project solve?
**Answer:**
In a Neonatal Intensive Care Unit (NICU), clinical data is often fragmented across multiple monitors and manual charts, increasing cognitive load and the risk of dosage calculation errors. This platform centralizes multiparametric telemetry, automates complex weight-based antibiotic protocols, logs structured data locally, and provides sandboxed AI decision support to streamline clinical documentation and improve safety workflows.

### 4. Who are the intended users?
**Answer:**
The platform models the complete operational medical hierarchy of a standard NICU. It implements a strict Role-Based Access Control (RBAC) architecture that dynamically alters user interface capabilities based on 5 professional profiles: Chief of Department (Șef de Secție), Attending Physicians, On-Call Physicians, Neonatologist Residents, and NICU Senior Nurses.

### 5. Why is neonatal sepsis important?
**Answer:**
Neonatal sepsis remains a leading cause of neonatal morbidity and mortality worldwide. Because its clinical presentation can be subtle and rapid, early identification within narrow windows and precise, weight-adjusted antibiotic interventions are absolutely critical to improve infant survival rates and reduce neurodevelopmental complications.

---

## Section 2 – Architecture & Presentation

### 6. Describe the system architecture.
**Answer:**
The application implements a decoupled, safety-critical hybrid architecture. It integrates a responsive Streamlit presentation layer, an operational telemetry data engine, a deterministic rule layer for bio-mathematical calculations, an isolated AI analysis wrapper, and a dual-persistence engine utilizing native SQLite connections for immediate dashboard reactivity alongside SQLAlchemy/Alembic blueprints for production readiness.

### 7. Why did you choose a modular architecture?
**Answer:**
A modular architecture enforces a strict Separation of Concerns (SoC). By isolating the presentation layer, the database schemas, the cryptographic authentication service, and the clinical guardrails into independent modules, the codebase becomes significantly easier to lint, debug, expand, and cover with automated regression tests.

### 8. What are the prominent components visible on the dashboard interface?
**Answer:**
* **Secure Cryptographic Access Gateway:** Role selection protected by constant-time signature validation.
* **CDSS Configuration Sidebar:** Controls for gestational profiles, weight inputs, and Family-Centered Care toggles.
* **Real-Time Vitals Grid:** Color-coded layout displaying heart rate, temperature, SpO2, and blood pressure.
* **Biomarker Kinetics Panel:** Visualization trackers for C-Reactive Protein (CRP) and Procalcitonin (PCT).
* **Deterministic Medication Engine:** Automated weight-based layouts calculating precise Ampicillin and Gentamicin limits.
* **Integrated Neuro-Musicotherapy Loop:** A functional audio player simulating low-frequency womb heartbeats for neurodevelopmental support.
* **Secure AI Support Workspace:** Tabbed interfaces displaying parsed, validated clinical reports.

---

## Section 3 – Security, Guardrails & RBAC

### 9. How did you implement authentication, and how does it prevent security bypasses?
**Answer:**
The system enforces cryptographic Role-Based Access Control (RBAC). Instead of exposing plaintext keys or storing passwords, the application evaluates tokens against 64-character hexadecimal **SHA-256 digests** loaded from the secure environment.
To block side-channel timing attacks (where an attacker attempts to guess a token bit-by-bit by measuring server response latencies), the validation routine utilizes `hmac.compare_digest()` to ensure execution occurs in constant time. If an environment variable is missing or malformed, the gateway defaults to a strict *fail-closed* state.

### 10. Large Language Models are non-deterministic. How do you guarantee clinical dosage safety?
**Answer:**
We implement a robust **Defense-in-Depth** pattern to ensure absolute safety:
1. **Deterministic Domination:** Medication doses are calculated entirely via immutable Python functions. The AI has zero control over these outputs.
2. **Post-Inference Semantic Guardrails:** The AI output is wrapped inside strict XML tokens (`<RAPORT>`, `<MEDICATIE>`, `<FCC>`). Before rendering text to the UI, the `NeonatalOutputGuardrail` class interceptor intercepts the payload. If the AI hallucinations breach the absolute neonatal ceiling (>500mg) or the weight-relative safety threshold (>150mg/kg), a `ClinicalGuardrailException` is raised. The interface instantly drops into a safe fallback mode, shielding the user from unsafe numbers.

---

## Section 4 – Testing, MLOps & CI/CD

### 11. How many tests does your project execute, and what do they validate?
**Answer:**
The project executes a comprehensive **26-test regression suite** via `pytest`, achieving deep coverage over critical application logic:
* `test_clinical_auth.py`: Verifies deterministic SHA-256 generation, constant-time validation paths, and error handling for non-string types.
* `test_system.py`: Validates the regex-based XML extraction engine, self-healing code blocks for omitted tags, absolute medication ceilings, and weight-relative anomalies.

### 12. What is Promptfoo, and how is it integrated into your MLOps workflow?
**Answer:**
Promptfoo is an open-source evaluation framework used to test LLM prompts, outputs, and security parameters. In this project, it is configured via `promptfoo.yaml` using a fast, local `echo` provider to execute a **9-scenario validation matrix**. It evaluates prompt injection resistance against malicious payloads (e.g., `ATTACK OVERRIDE`), layout structural rules, and multilingual consistency across 6 different languages (EN, RO, IT, DE, FR, ES) directly within the terminal via `uv run promptfoo eval`.

### 13. Describe your Continuous Integration (CI/CD) pipeline.
**Answer:**
The project uses GitHub Actions to automate two discrete quality gates:
1. **Code Quality & Testing:** Triggered on push or pull request, it sets up an ultra-fast `uv` environment, executes strict static code analysis and formatting checks using `ruff`, and runs the 26 `pytest` regression scenarios.
2. **Container Image Integrity Matrix:** It runs an automated build check using Docker Buildx to compile the multi-stage `Dockerfile` in the cloud. This verifies container integrity and dependency locking without requiring local Docker installations.

---

## Section 5 – Senior Engineering Architectural Choices

### 14. Why did you use raw SQL connections inside app.py if you have an active SQLAlchemy and Alembic schema setup?
**Answer:**
This is an intentional design choice optimizing for performance and state rendering. Streamlit operates on a reactive rendering model, rerunning the entire script execution file upon any user widget interaction. Using a heavy Object-Relational Mapper (ORM) transaction lifecycle inside the core UI loop introduces unnecessary connection setup and resource allocation overhead. By leveraging native, thread-safe raw SQL connections via Python's built-in `sqlite3` driver inside `app.py`, telemetry commits and data reads execute with negligible rendering latency, while SQLAlchemy and Alembic are retained in separate modules to ensure schema portability and versioning integrity for future production-grade migrations.

### 15. I noticed you appended `# type: ignore` annotations next to core library imports. Why?
**Answer:**
The `# type: ignore` overrides are localized static-analysis annotations introduced exclusively to address a path-mapping synchronization discrepancy between the local virtual environment (`.venv`) and global type checkers (like Pylance) in certain IDE workspaces on Windows. The underlying environment and dependency locking are fully intact, which is proven by the clean validation matrix from **Ruff** and the fact that the entire test suite compiles and executes with zero errors.
