# Security Policy

## 🛡️ Defensive Cybersecurity Research & Synthetic Data Notice

This repository is an **educational application security (AppSec) postmortem, test harness, and compiler parsing evaluation suite** published under the MIT License.

* **100% Synthetic Mock Data:** This repository contains **NO** video files, **NO** camera footage, **NO** audio recordings, **NO** images, **NO** private IP addresses, and **NO** real personal data (PII). All telemetry logs and timestamps are synthetic simulations.
* **Defensive Purpose:** Published strictly to assist systems engineers and AI developers in preventing Broken Object Level Authorization (BOLA / OWASP API1) and lexical token collision bugs (the Scunthorpe problem) in autonomous agents.

---

## 📋 Supported Versions

We actively maintain the latest state on the `main` branch:

| Version / Branch | Supported          |
| :--------------- | :----------------- |
| `main`           | :white_check_mark: |
| Older releases   | :x:                |

---

## 🚨 Reporting a Vulnerability

If you discover a security vulnerability, prompt parsing bypass, or an unhandled edge case that could lead to unauthorized tool execution in system agent architectures:

1. **Do NOT open a public GitHub issue.**
2. Report the vulnerability privately via **GitHub Private Vulnerability Reporting** (Security tab -> "Report a vulnerability").
3. Alternatively, contact the maintainers directly via email: `nemospecialis@gmail.com`.

### What to Include:
* A description of the parsing flaw or authorization bypass.
* A minimal, reproducible Python test script demonstrating the issue using synthetic mock data.
* Potential remediation suggestions.

### Our Commitment:
* We will acknowledge receipt of your report within **48 hours**.
* We will provide an assessment and work on a verified fix.
* Once patched, you will be credited in the repository's postmortem release notes (unless you prefer anonymity).
