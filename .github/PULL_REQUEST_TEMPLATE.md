## Description
Briefly explain the goal of this pull request, the problem it solves, and the changes introduced.

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue in a parser or test harness)
- [ ] New feature / example (adding a new reproduction or architectural defense)
- [ ] Documentation update (improving the postmortem analysis or README)
- [ ] Telemetry or CI improvement

## Checklist
- [ ] **100% Synthetic Data:** My changes contain zero real video footage, zero personal media, and zero real PII.
- [ ] **Zero Dependencies:** All example scripts run purely on standard Python 3.10+ without third-party pip requirements.
- [ ] **Local Verification:** All example scripts pass cleanly:
  ```bash
  python3 examples/01_vulnerable_parser.py
  python3 examples/02_hardened_parser.py
  python3 examples/03_rfc5322_threading.py
  python3 examples/04_modality_decoupled_ingress.py
  ```
- [ ] **Documentation:** Relevant sections in `README.md` have been updated to reflect any new concepts or options.
