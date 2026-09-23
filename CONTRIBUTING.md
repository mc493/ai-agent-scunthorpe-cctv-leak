# Contributing to AI Agent Scunthorpe & BOLA Postmortem

Thank you for your interest in contributing to this educational AppSec research project and reproduction test suite!

---

## 🛡️ Core Contribution Principles

This project is an **educational postmortem and compiler/parsing evaluation suite**. To preserve research integrity and data safety, all contributions must uphold these non-negotiable rules:

1. **100% Synthetic & Mock Data Only:**
   - **NO real personal data (PII):** Do not submit real names, home addresses, phone numbers, or private emails.
   - **NO real camera media:** Do not commit video files, camera feeds, screenshots of physical premises, or private IPs.
   - All tests and fixtures must use synthetic identifiers (e.g., `operator@example.com`, `driveway_cctv`, `track_id: 412`).

2. **Zero Dependencies for Reproduction Examples:**
   - All scripts under `examples/` must run purely on the **Python 3.10+ standard library** without requiring third-party pip packages (e.g. `requests`, `fastapi`, `pydantic`).

3. **Responsible Disclosure:**
   - If you discover an unhandled parser bypass or security vulnerability, please follow our [Security Policy](SECURITY.md).

---

## 🛠️ Development & Testing Workflow

1. **Fork and Clone:**
   ```bash
   git clone https://github.com/<your-username>/ai-agent-scunthorpe-cctv-leak.git
   cd ai-agent-scunthorpe-cctv-leak
   ```

2. **Create a Feature Branch:**
   ```bash
   git checkout -b fix/parser-edge-case
   ```

3. **Run the Test Suite:**
   Ensure all existing standalone example harnesses execute cleanly with zero errors:
   ```bash
   python3 examples/01_vulnerable_parser.py
   python3 examples/02_hardened_parser.py
   python3 examples/03_rfc5322_threading.py
   python3 examples/04_modality_decoupled_ingress.py
   ```

4. **Verify Telemetry Archival:**
   ```bash
   python3 scripts/archive_traffic.py
   ```

---

## 📝 Commit Message Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

* `feat:` A new example harness or architectural defense pattern.
* `fix:` A bug fix in parser regexes or threading constructors.
* `docs:` Documentation improvements or postmortem analysis additions.
* `test:` Adding new parser test fixtures or edge-case validation.
* `chore:` Maintenance, GitHub Actions, or badge telemetry updates.

---

## 🚀 Submitting a Pull Request

1. Push your branch to GitHub.
2. Open a Pull Request against the `main` branch.
3. Fill out the provided [Pull Request Template](.github/PULL_REQUEST_TEMPLATE.md), confirming that all data is synthetic and tests pass.
4. Maintainers will review your submission promptly.
