# Security Policy

## Defensive Cybersecurity Research & Synthetic Data Notice

This repository is an **educational application security (AppSec) postmortem, test harness, and compiler parsing evaluation suite** published under the MIT License.

* **100% Synthetic Mock Data:** This repository contains **NO** video files, **NO** camera footage, **NO** audio recordings, **NO** images, **NO** private IP addresses, and **NO** real personal data (PII). All telemetry logs and timestamps are synthetic simulations.
* **Defensive Purpose:** Published strictly to assist systems engineers and AI developers in preventing Broken Object Level Authorization (BOLA / OWASP API1) and lexical token collision bugs (the Scunthorpe problem) in autonomous agents.

---

## Supported Versions

The latest state is actively maintained on the `main` branch:

| Version / Branch | Supported          |
| :--------------- | :----------------- |
| `main`           | Yes |
| Older releases   | No                |

---

## Reporting a Vulnerability

If you discover a security vulnerability, prompt parsing bypass, or an unhandled edge case that could lead to unauthorized tool execution in system agent architectures:

1. **Do NOT open a public GitHub issue.**
2. Report the vulnerability privately via **GitHub Private Vulnerability Reporting** (Security tab -> "Report a vulnerability").
3. Alternatively, contact the maintainers directly via email: `nemospecialis@gmail.com`.

### What to Include:
* A description of the parsing flaw or authorization bypass.
* A minimal, reproducible Python test script demonstrating the issue using synthetic mock data.
* Potential remediation suggestions.

### Response Policy:
* Receipt of reports is acknowledged within **48 hours**.
* Security assessment and fix verification are conducted proactively.
* Once patched, credit is provided in the repository release notes (unless anonymity is preferred).
