# 📝 Changelog: Sepsis Monitor AI

All notable changes to this project are documented in this file. This repository adheres to Semantic Versioning (`MAJOR.MINOR.PATCH`).

---

## - 2026-10-30

### ✨ Added
- **Constant-Time Cryptographic RBAC Gateway:** Integrated a secure access perimeter inside `auth_service.py` that validates tokens using 64-character hexadecimal SHA-256 digests and `hmac.compare_digest()` to completely block side-channel timing analysis attacks.
- **Fail-Closed Security Posture:** Configured startup validation logic to automatically fail closed and lock the user interface if necessary environment variables are missing, malformed, or retain placeholders.
- **Enhanced Guardrails Unit Testing:** Added absolute ceiling checks (`>500mg`) and relative weight-based dosage validation scenarios (`>150mg/kg`) into the automated test matrix.
- **Streamlit In-App Promptfoo Indicator:** Wired the sidebar component to read local evaluation matrices, dynamically displaying a green execution status badge (`✓ Automated Matrix: 100% Defense Compliance`) upon successful assertions matching.

### 🐛 Fixed
- **Ruff Import Block Violation (I001):** Reorganized and sorted all project-wide imports alphabetically and inside discrete standard/third-party library blocks in accordance with the `isort` specification, clearing all Ruff I001 warnings.
- **Regex Parsing Unification:** Refactored the flexible extraction mock utility inside `tests/test_system.py` to use regular expressions (`re.search`) rather than string slicing (`.split`), mirroring the live deployment configuration used in `app.py`.
- **Unicode Hidden Character Cleansing:** Purged broken encoding anomalies, Windows carriage artifacts (`\r\n` bugs), and invalid non-breaking spaces (`\ua0`) from configuration templates and script markdowns to ensure seamless bare-metal compilation.

---

## - 2026-08-10

### ✨ Added
- **Synchronous Regex Gateway Firewall:** Engineered a backend validation security layer using strict word boundaries `\b(IGNORE|OVERRIDE|CLEAN|SYSTEM RESET)\b` inside `app.py` to intercept and neutralize adversarial prompt injection vectors before API serialization.
- **Multi-Stage Automated CI/CD Pipelines:** Deployed an enterprise-grade GitHub Actions pipeline under `.github/workflows/ci.yml` and `mlops.yml` that configures automated `uv` environments, runs style enforcement checks via `ruff`, and builds isolated Docker Buildx validation images in the cloud.
- **Persistent Cyber Alert Architecture:** Integrated `st.session_state["cyber_alert_triggered"]` to ensure a permanent warning block renders on the clinician control board if a prompt hijacking attempt is blocked.
- **XML Self-Healing Infrastructure:** Added validation capabilities within `src/guardrails/guardrails.py` to automatically inject missing layout blocks (such as an omitted `<FCC>` tag) back into the text context to guarantee downstream UI parsing stability.

### 🐛 Fixed
- **Unreachable Dead Code Purge:** Cleaned conditional logical branches and redundant statements inside `sanitize_clinical_payload` that were causing unreachable code execution blocks.
- **Streamlit Reactive Rendering:** Integrated native `st.rerun()` gates inside the core database transactional control blocks (`Execute Telemetry Step` and `Simulate Injection Therapy`), fixing layout rendering latencies and forcing instantaneous data chart refreshes.
- **Regression Matrix Expansion:** Expanded the automated testing pyramid to reach **26 passed scenarios**, covering model fields, transactional rollbacks, security firewalls, and context-drifting anomalies.

---

## - 2026-08-04

### ✨ Added
- **Individualized Weight-Based Dose Calculator:** Deployed a strict bio-mathematical calculation engine inside the dashboard workspace computing customized antibiotic regimes (Ampicillin and Gentamicin limits matching infant mass records from `0.50 kg` to `6.00 kg`).
- **Active Acoustic Neuro-Stabilization Loop:** Added background streaming capabilities inside Streamlit to play a continuous auditory womb sensory file (`womb_heartbeat.mp3`) from local file storage when Music Therapy is enabled.
- **In-Memory Diskless Report Compiler:** Integrated on-the-fly binary ReportLab canvas generation using `io.BytesIO` that packs historical records, telemetry schemas, and weight-adjusted micro-dosages directly into secure memory buffers, preventing data caching leaks.
- **Embedded Document Gateway:** Implemented a secure base64 HTML iframe embedding solution to display real-time clinical report previews directly on the dashboard screen with native zoom, scroll, and print controls.
- **Relational Data Layer Persistence:** Configured transactional connection pools utilizing local SQLite instances (`sepsis_neonatal.db`) for secure hourly data logging.
