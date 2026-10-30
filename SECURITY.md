# 🛡️ SECURITY POLICY & HARDENING BOUNDS: SEPSIS MONITOR AI

## 1. Purpose and Scope

This document defines the active security controls, data-handling policies, LLM guardrails, automated regression testing procedures, and cryptographic deployment boundaries engineered into the Sepsis Monitor AI platform.

The application operates as a portfolio-grade Clinical Decision Support System (CDSS) prototype. The security controls detailed herein are implemented to mitigate operational vulnerabilities and demonstrate sandboxed safety workflows. They reflect the current source code, dependency configurations, and continuous integration pipeline results.

---

## 2. Reporting a Vulnerability

Do not close or disclose exploitable vulnerability details within public GitHub issues or open pull requests.

Report security concerns, logic bypasses, or potential vulnerabilities directly to the project author via the verified contact channels maintained on the primary [Maria Gabriela Cojocaru](https://github.com) repository matrix.

When submitting a security report, provide:
- A concise description of the affected module or boundary layer.
- Step-by-step instructions or test payloads required to reproduce the behavior.
- Sanitize logs or evidence; do not include API keys, active tokens, or real data.

---

## 3. Core Security Architecture & Perimeter Hardening

The application enforces a rigorous, multi-tiered security architecture protecting both the local data plane and the generative model inference cycle.

### 3.1. Input Validation and Prompt-Injection Defense
- **Type-Strict Parameter Validation:** All clinical parameters (infant weight, biomarker kinetics, and vital signs) are validated against explicit data types and enforced bounds on the server side. Weight variables are mathematically constrained to a strict `0.50 kg` to `6.00 kg` operational spectrum.
- **Defense-in-Depth Pipeline:** The system treats all textual inputs as completely untrusted vectors. Malicious string patterns are filtered using localized pattern matching before payloads contact downstream clinical evaluation code.

### 3.2. Role-Based Access Control (RBAC) Criptography
- **SHA-256 Verified Digests:** The system rejects plaintext access keys. Interface roles are decoupled and authenticated against pre-computed, 64-character hexadecimal **SHA-256 hashes** loaded at runtime from environment variables.
- **Timing-Attack Mitigation:** Token validation uses `hmac.compare_digest()`. This forces evaluation paths to execute in constant time, neutralizing side-channel timing analysis attacks designed to guess keys bit-by-bit.
- **Fail-Closed Default:** If an environment signature variable is missing, blank, or retains template placeholders, the gateway activates a strict *fail-closed* state, locking down the downstream UI state.

### 3.3. LLM Guardrails and Output Validation
- **Deterministic Math Domination:** All critical antibiotic dosing recommendations (Ampicillin and Gentamicin) are calculated entirely within hardcoded Python rule engines. The LLM has zero operational permission to define or alter medication volumes.
- **Post-Inference Boundary Interception:** Generative responses must comply with rigid XML token frames (`<RAPORT>`, `<MEDICATIE>`, `<FCC>`). Before UI injection, the `NeonatalOutputGuardrail` class parses the blocks using regular expressions. If it detects a hallucinated boundary violation—breaching the absolute ceiling (`>500mg`) or weight-relative threshold (`>150mg/kg`)—it raises a `ClinicalGuardrailException`. The system intercepts the workflow, suppresses the output, and renders a safe, hardcoded error canvas.

### 3.4. Continuous Integration Security Quality Gates
Continuous security monitoring is automated via GitHub Actions utilizing two isolated jobs inside `.github/workflows/ci.yml`:
- **Static Security Audits:** Runs `ruff` to perform static code analysis and block architectural smells or syntax weaknesses.
- **Deterministic Test Matrices:** Executes a comprehensive **26-scenario `pytest` matrix** ensuring that cryptographic service gates, invalid data inputs, and database rollback scopes function as expected.

---

## 4. Automated Security Testing Execution

### 4.1. Code Quality and Static Checks
Execute the unified linter suite locally to guarantee style compliance and zero code-quality regressions:
```bash
uv run ruff check . --fix
```

### 4.2. Promptfoo Red-Team Evaluation
The MLOps pipeline embeds **Promptfoo** to execute a sandboxed **9-point assertion matrix** configured inside `promptfoo.yaml`. It uses a zero-latency `echo` provider to ensure that prompt injection payloads (e.g., `ATTACK OVERRIDE`) are systematically caught and structural XML tags are preserved across all locales (EN, RO, IT, DE, FR, ES) without execution leaks:
```bash
uv run promptfoo eval -c promptfoo.yaml
```

---

## 5. Clinical Disclaimer and Limitations

Sepsis Monitor AI is an educational demonstration prototype. It has not been clinically validated, audited for regulatory medical software frameworks, or certified for hospital environment deployment.

Generative model responses can contain inaccuracies, hallucinations, or contextual inconsistencies. Human medical judgment, physical verification of clinical charts, and authoritative institutional protocols must always supersede any information presented on this dashboard. Do not use this application to inform actual real-world diagnosis, treatment strategies, or infant medication dosing.

---

## 6. Author and Maintenance

**Project Author:** Cojocaru Maria Gabriela
**Compliance Profile:** Written in accordance with PEP 8, PEP 257, and the Ruff code quality standard. Security models are reviewed and updated alongside modifications to the cryptographic validation layers or MLOps automation flows.
