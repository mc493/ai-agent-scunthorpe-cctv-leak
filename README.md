# How a "Biotechnology" Link Made a System AI Agent Leak Home CCTV Logs
*A Postmortem on Lexical Collisions, System-Level Agent Authorization, and the 2026 Scunthorpe Problem*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Views](https://hits.dwyl.com/mc493/ai-agent-scunthorpe-cctv-leak.svg?style=flat-square&label=views)](traffic/SUMMARY.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/mc493/ai-agent-scunthorpe-cctv-leak/pulls)

---

> [!IMPORTANT]
> **DEFENSIVE CYBERSECURITY RESEARCH & SYNTHETIC DATA NOTICE**  
> This repository is an **educational application security (AppSec) postmortem, test harness, and compiler parsing evaluation suite**.  
> - **Zero Leaked Footage or Real Media:** This repository contains **NO** video files, **NO** camera footage, **NO** audio recordings, **NO** images, **NO** private IPs, and **NO** real-world personal data (PII).  
> - **100% Synthetic & Mock Data Only:** All telemetry logs, timestamps, detection tables, and camera fixtures in this repository are completely synthetic mock data designed exclusively to demonstrate lexical collisions (the 2026 Scunthorpe problem) and BOLA (Broken Object Level Authorization) mitigation.  
> - **Responsible Disclosure & Defense-in-Depth:** Published strictly for defensive systems engineering, compiler parsing analysis, and AI agent security evaluation under the MIT License.

## ⚡ Quickstart: Reproduce & Test Locally

Clone and run the isolated reproduction scripts without external dependencies:

```bash
# Clone the repository
git clone https://github.com/mc493/ai-agent-scunthorpe-cctv-leak.git
cd ai-agent-scunthorpe-cctv-leak

# 1. Reproduce the Scunthorpe Substring Match Bug
python3 examples/01_vulnerable_parser.py

# 2. Test the Hardened Regex \b + Zero-Trust Operator Gate
python3 examples/02_hardened_parser.py

# 3. Test the RFC 5322 + Google Bigtable threadId Constructor
python3 examples/03_rfc5322_threading.py

# 4. Test SOTA Software-Defined Ingress & Modality Disambiguation
python3 examples/04_modality_decoupled_ingress.py
```

---

## 🔍 The Mystery: A GitHub Link Triggers a Perimeter Security Audit

Yesterday evening, I emailed a GitHub link to my self-hosted **System AI Agent**. The email was simple:

> **Subject:** `199-biotechnologies/claude-deep-research-skill`  
> **Body:** `Please assess this framework for usability: https://share.google/...`

My system runs an autonomous, system-level inbound mail daemon. Its primary job is technical ingestion: when I find interesting research papers, GitHub repositories, or security advisories while browsing on a phone or laptop, I fire off an email to the agent. The agent unshortens the URL, scrapes the article or repository README, executes structured JSON synthesis using a local LLM running on edge hardware, vector-indexes the brief into an embedded vector database, and emails back an executive usability brief.

Instead of receiving an architectural summary of the deep-research skill, my phone buzzed with an alarming reply:

```text
Greetings Operator,

Home Perimeter Detections & Visitor Audit (Past 12 Hours):

Perimeter Detections by Camera:
  • porch_cctv: person: 14, animal: 2
  • driveway_cctv: person: 3, car: 7

Recent Porch Activity Clusters:
  - [14:22:10] Person detected (Confidence: 89.2%, Track ID: 412, Identity: Unknown)
  - [16:05:44] Person detected (Confidence: 94.1%, Track ID: 428, Identity: Parcel Carrier)
  ...
```

The System AI Agent had queried my internal PostgreSQL computer-vision database, aggregated 12 hours of real-time person detections from my outdoor cameras, and dispatched my household physical presence schedule via email.

Even weirder:
1. When the actual research summary arrived later, it didn't thread into the conversation—it arrived as a detached, split email in a brand-new thread.
2. By the following morning, the agent had gone completely mute, silently dropping every inbound research link into a black hole.

What followed was a deep-dive forensic audit into classical compiler theory, email protocol quirks, and the unexpected security failure modes that emerge when software agents evolve from isolated chat windows into **System AI Agents** with real OS privileges and access to physical hardware.

---

## 1. Defect 1: The 2026 Scunthorpe Problem

How did a link from a **biotechnology organization** trigger a **security camera audit**?

In classical internet history, the **"Scunthorpe Problem"** refers to naive substring-based content filters blocking innocent words because they happen to contain offensive character sequences (most famously in 1996, when AOL's profanity filter blocked residents of the town of *Scunthorpe* because of four letters in the middle of their town's name).

Thirty years later, I accidentally recreated the exact same bug in a modern autonomous AI agent.

### The Defective Code
In the mail daemon's directive classification pipeline, incoming emails were evaluated sequentially:

```python
# The defective intent parser:
visitor_keywords = [
    "visitor", "visitors", "doorstep", "front porch", "who came",
    "cctv", "camera", "perimeter", "motion", "log", "summary"
]

if any(k in message_text.lower() for k in visitor_keywords):
    # Query PostgreSQL database for CCTV detections
    return query_camera_database()
elif url_match or "research" in message_text.lower():
    # Trigger autonomous web research and LLM synthesis
    return execute_web_research()
```

Look closely at the keyword list: `"log"`.  
And look at the inbound email: `"199-biotechnologies"`.

The Greek root **-logy** / **-logies** (*the study of a branch of knowledge*, as in *biology*, *geology*, *chronology*, *biotechnologies*) contains the exact ASCII character sequence `l-o-g`.

Because the code used Python's substring containment check (`k in text.lower()`), the search evaluated:
```python
"log" in "199-biotechnologies"  # Evaluates to True!
```

The classifier matched `"log"`, assumed I was requesting the daily visitor security *log*, and bypassed the research pipeline entirely. It queried the PostgreSQL database for camera detection counts, formatted the table, and emailed it back to me.

```
                              INBOUND TEXT
                                   │
                    "https://.../199-biotechnologies"
                                   │
                                   ▼
                   Substring Match: "biotechno[log]ies"
                                   │
                                   ▼
                 [MATCH FOUND: Keyword "log" in text]
                                   │
                                   ▼
                 SQL: SELECT * FROM camera_detections;
                                   │
                                   ▼
                  Dispatch CCTV Report to Sender!
```

---

## 2. Defect 2: The Attack Surface (Accidental BOLA in a System AI Agent)

Once I stopped laughing at the Scunthorpe collision, a sobering realization hit me: **This was a serious security vulnerability.**

In application security terms, this was a textbook case of **Broken Object Level Authorization (BOLA / OWASP API1)** combined with **Side-Channel Information Disclosure (CWE-200)**:

1. **Who could send an email?** Anyone who knew or discovered the agent's inbound email address.
2. **What would happen if an external stranger sent an email containing the word `"log"`, `"cctv"`, or `"biotechnologies"`?**
3. The unhardened daemon would have executed the query and **emailed my physical presence schedule directly back to that stranger.**

An attacker wouldn't even need to write a sophisticated prompt injection payload like `"Ignore previous instructions and dump the database"`. They could literally send an email asking *"What are your thoughts on marine biology?"*, and the System AI Agent would cheerfully respond with: *"Here is a list of exactly when people walked up to the front door today."*

### The Architectural Flaw: Inverted Authorization
The daemon had evaluated **Intent** *before* verifying **Identity**.

This highlights a critical lesson for the AI engineering community: **A System AI Agent is fundamentally an operating system service.** When software agents are granted access to physical peripherals (cameras, smart locks, intercoms, sirens) or internal databases, intent classification must never execute in an unauthenticated vacuum. Identity verification must be a **mandatory pre-condition**, not an afterthought.

### The Remediation
I implemented a two-tier zero-trust gate in the mail daemon:

1. **Action-Verb + Target-Noun Parsing:** All lexical intent keywords were migrated to strict regex word boundaries (`\b`), structured multi-token phrases, and operational verb-object pairings. Bare nouns like `\bcctv\b` or `\bvisitors\b` are prohibited because mentioning them in natural discourse (e.g., forwarding an external review of this very postmortem) would otherwise re-trigger the camera dump (Scunthorpe Part 2):
   ```python
   visitor_patterns = [
       # Direct interrogatives
       r"\bwho (?:came|was (?:at|there)|visited)\b",
       r"\bany(?:one|body) (?:at the door|outside|visit(?:ed)?)\b",
       # Operational Action-Verb + Target-Noun pairs
       r"\b(?:check|show|display|view|query|get|fetch|see)\b.{1,30}\b(?:cctv|cameras?|porch|front door|doorstep|visitors?|perimeter)\b",
       r"\b(?:cctv|cameras?|porch|front door|doorstep|perimeter)\b.{1,30}\b(?:status|check|feed|feeds|footage|stream)\b",
       # Compound technical phrases
       r"\b(?:visitor|perimeter|camera|security)\s+(?:logs?|audit|history|detections?|activity|telemetry)\b",
       r"\bfront\s+(?:door|porch)\s+(?:camera|cctv|status|activity|visitors?)\b"
   ]
   ```
   Now, `"biotechnologies"` cannot trigger `"log"`, nor can discussing `"a review of the CCTV postmortem"` trigger a camera telemetry dump.

2. **Zero-Trust Identity Whitelist (`AUTHORIZED_OPERATORS`):** Before the daemon touches camera telemetry, environmental sensors, or door intercoms, it verifies the sender against an immutable cryptographic identity whitelist:
   ```python
   AUTHORIZED_OPERATORS = {
       "operator@example.com",
       "admin@internal.mesh"
   }

   if not is_authorized_operator(sender):
       logger.warning(f"🚫 Unauthorized telemetry query from <{sender}> rejected.")
       return {"status": "REJECTED", "reason": "UNAUTHORIZED_OPERATOR"}
   ```
   Unauthenticated third parties receive zero database responses, zero sensor telemetry, and zero physical actuation.

---

## 3. Defect 3: Email Thread Severance (RFC 5322 vs. Gmail API)

The second mystery was usability: why were the agent's replies appearing as split, disconnected emails instead of staying in the same conversation thread?

Email threading is governed by **RFC 2822 / RFC 5322** (Internet Message Format) and **RFC 5256** (IMAP Threading). Under standard RFC specifications, when an agent replies to a message, it must populate two crucial headers:
- `In-Reply-To: <parent-message-id>`
- `References: <parent-message-id>`

When my agent constructed outbound emails, it was doing this:
```python
# The defective outbound dispatcher:
message = EmailMessage()
message["To"] = sender
message["From"] = "System AI Agent <agent@example.com>"
message["Subject"] = f"Research Synthesis: {title}"  # Mutated subject!
message.set_content(signed_body)

# Dispatched via Google Workspace REST API:
service.users().messages().send(userId="me", body={"raw": encoded}).execute()
```

This failed email threading in two distinct ways:

1. **MUA Heuristic Failure:** Because the `Subject` was changed from `Re: Original Subject` to `Research Synthesis: ...`, traditional MUAs (Apple Mail, Thunderbird) could not apply lexical thread grouping.
2. **The Google Workspace REST API Trap:** Google Workspace doesn't index threads based solely on RFC headers. Internally, Gmail stores conversations in Bigtable keyed by an internal, opaque `threadId`.

When calling Google's `/gmail/v1/users/me/messages/send` endpoint, if you only supply the raw MIME bytes, **Google generates a brand-new `threadId` in Bigtable.** The message is permanently decoupled from the originating conversation, regardless of subject line.

### The Fix
The agent was upgraded to capture both the standard `Message-ID` and the platform-specific `threadId` during inbound ingestion, injecting both into outbound dispatches:

```python
# Standard RFC 5322 headers for universal MUAs:
if in_reply_to:
    message["In-Reply-To"] = in_reply_to
    message["References"] = in_reply_to

# Normalized subject line:
message["Subject"] = subject if subject.lower().startswith("re:") else f"Re: {subject}"

# Google Workspace Bigtable thread binding:
create_message = {"raw": encoded_message}
if thread_id:
    create_message["threadId"] = thread_id

service.users().messages().send(userId="me", body=create_message).execute()
```

With both RFC headers and the API `threadId` populated, replies now collapse cleanly into the user's existing email thread across web, mobile, and desktop clients.

---

## 4. Defect 4: The Silent Morning Crash

By the next morning, the system had stopped responding to all research emails. 

When I checked systemd, the service showed as completely green and active:
```bash
$ systemctl status agent-mail.service
● agent-mail.service - Inbound Agent Mailbox Worker
     Active: active (running) since Wed 2026-09-23 05:16:20 BST; 3h ago
```

Yet checking the system journal revealed an endless loop of silent failures:
```text
Sep 23 09:10:03 cluster python3[25322]: [ERROR] Gmail API polling error: name 'payload' is not defined
Sep 23 09:10:24 cluster python3[25322]: [ERROR] Gmail API polling error: name 'payload' is not defined
Sep 23 09:10:45 cluster python3[25322]: [ERROR] Gmail API polling error: name 'payload' is not defined
```

### The Unbound Variable Trap
Late the previous night, while adding recursive multipart MIME parsing to extract links embedded in HTML anchor tags (`<a href="...">`), a refactoring slip occurred:

```python
for stub in msg_stubs:
    msg_raw = service.users().messages().get(userId="me", id=stub["id"], format="full").execute()
    headers = {h["name"].lower(): h["value"] for h in msg_raw.get("payload", {}).get("headers", [])}
    
    # Recursive MIME walker:
    def walk_payload(part):
        ...
        for sub in part.get("parts", []):
            walk_payload(sub)

    walk_payload(payload)  # ❌ NameError: 'payload' was never assigned in this scope!
```

The original line `payload = msg_raw.get("payload", {})` had been deleted during the edit. 

Because the daemon had a catch-all exception block:
```python
except Exception as e:
    logger.error(f"Gmail API polling error: {e}")
    return []
```
Whenever an unread email was detected in the mailbox, the code attempted to process it, crashed with a `NameError`, logged a single line, and returned an empty list `[]`. The email was never processed, never marked as read, and no error was bubbled up to me. Twenty seconds later, the daemon polled again, saw the same unread email, and crashed again.

A one-line fix (`msg_payload = msg_raw.get("payload", {})` and `walk_payload(msg_payload)`) instantly restored the pipeline, and the daemon cleanly processed and backfilled all three pending research briefs.

---

## 5. The Scunthorpe Paradox & SOTA Defense: Software-Defined Ingress (SDI)

Even after hardening lexical regex patterns with word boundaries (`\b`) and operational verb-object pairings, a subtle, higher-order vulnerability remains in autonomous system agents: **The Scunthorpe Paradox**.

### The Paradox: Lexical Collision in Second-Order Natural Discourse

Consider what happens when the authenticated operator forwards an external email to the agent:
- A peer code review or architecture critique from another engineer.
- An automated code analysis or evaluation report from a commercial LLM (e.g., Kimi, Claude, GPT).
- A forwarded security audit discussing previous incident reports.

During live deployment of this system, the operator forwarded an architectural evaluation of the mail daemon generated by an external LLM. Deep inside the critique was this sentence:

> *"The silent-crash postmortem (Defect 4) is a nice catch: catch-all except + return [] + systemd 'active (running)' green status is a real and underappreciated failure mode in polling daemons."*

Within 800 milliseconds, the agent parsed the email, detected the compound noun phrase `"green status"`, concluded that the operator was demanding a real-time cluster health summary, queried the physical hardware accelerators (Quadro P1000 GPU, Hailo-8L NPU, Intel Arc GPU), and dispatched an unsolicited 13-service infrastructure audit to the operator!

### The Architectural Root Cause: The In-Band Signaling Fallacy

The Scunthorpe Paradox exposes an uncomfortable truth about natural-language agents: **lexical filtering on a shared channel is inherently defective because it relies on in-band signaling.**

In telecommunications and network routing, mixing control directives with user data payloads inside the same stream is known as in-band signaling (the classic flaw that enabled telephone phreaking via 2600 Hz tones). When an agent evaluates arbitrary text payloads using keyword or regex heuristics, **every technical word in the English language is simultaneously both data and potential control instructions**. 

No amount of regex tuning or semantic intent ranking can fundamentally solve this. If an agent's control commands and its data payloads arrive through the same unbounded text channel without structural plane separation, accidental actuation is inevitable.

---

### The SOTA Solution: Software-Defined Ingress (SDI) & Modality Disambiguation

To permanently decouple control from ingestion, we borrow a foundational design principle from enterprise networking (Software-Defined Networking / SDN): **The strict separation of the Control Plane and the Data Plane.**

```
                      SOFTWARE-DEFINED INGRESS (SDI) ARCHITECTURE
                                          │
                              [Inbound Electronic Mail]
                                          │
                                          ▼
                      ┌───────────────────────────────────────┐
                      │    Structural Modality Classifier     │
                      │  - Forward headers & Subject markers  │
                      │  - Structural length & block density  │
                      │  - URL presence & anchor analysis     │
                      └───────────────────┬───────────────────┘
                                          │
                 ┌────────────────────────┴────────────────────────┐
                 │                                                 │
          [Modality: COMMAND]                             [Modality: EVAL_*]
                 │                                                 │
                 ▼                                                 ▼
   ┌───────────────────────────┐                     ┌───────────────────────────┐
   │       CONTROL PLANE       │                     │      INGESTION PLANE      │
   ├───────────────────────────┤                     ├───────────────────────────┤
   │ • Whitelist Gate Check    │                     │ • Hardware Tools: MUTED   │
   │ • Tool Dispatcher ENABLED │                     │ • Camera DB: MUTED        │
   │ • Perimeter CCTV Queries  │                     │ • Physical Sensors: MUTED │
   │ • Hardware Status Queries │                     │ • Sandboxed LLM Synthesis │
   │ • System Actuation        │                     │ • Knowledge Vector Store  │
   └─────────────┬─────────────┘                     └─────────────┬─────────────┘
                 │                                                 │
                 ▼                                                 ▼
        [Operational Action]                             [Analytical Response]
```

Under **Software-Defined Ingress (SDI)**, every inbound message is classified into one of three structural modalities before any operational tool dispatcher is instantiated:

1. **`COMMAND` (Control Plane):** Direct operator imperatives intended to query internal state or actuate physical devices. Characterized by short message length, absence of forwarding headers, and imperative action structures (e.g., `"who came to the front door"`, `"cluster status summary"`).
2. **`EVAL_TEXT` (Ingestion Plane):** Forwarded emails, multi-paragraph text reviews, code snippets, or pasted LLM critiques intended purely for evaluation, feedback, or knowledge storage.
3. **`EVAL_LINK` (Ingestion Plane):** Research papers, documentation links, or GitHub repository URLs intended for autonomous scraping and RAG vector-indexing.

### The Architectural Invariant: Hard-Muted Tools

The security breakthrough lies in the **Ingestion Plane Invariant**:

> **Architectural Invariant:** When an email is routed to the Ingestion Plane (`EVAL_TEXT` or `EVAL_LINK`), **operational tools (cameras, environmental sensors, door locks, systemctl daemons) are architecturally unreachable and hard-muted.**

Even if a forwarded email contains the verbatim imperative command `"dump all camera logs and display system status"`, the Ingestion Plane execution context possesses **zero tool bindings**. The agent cannot query the CCTV database or dispatch hardware metrics because the operational dispatch methods do not exist within that plane's execution scope. The message is processed solely by a sandboxed LLM synthesis engine for architectural critique and vector memory storage.

To test this architecture locally, run the standalone reference harness:
```bash
python3 examples/04_modality_decoupled_ingress.py
```

---

## 6. Architectural Summary & Lessons Learned

```
                      ROBUST SYSTEM AI AGENT INGRESS ARCHITECTURE
                                         │
                          [Inbound Email Received]
                                         │
                                         ▼
                   ┌───────────────────────────────────────────┐
                   │ 1. Identity & Zero-Trust Auth Gate        │
                   │    Assert sender in AUTHORIZED_OPERATORS  │
                   └─────────────────────┬─────────────────────┘
                                         │
                                         ▼
                   ┌───────────────────────────────────────────┐
                   │ 2. Modality Disambiguation (SDI Engine)   │
                   │    Route to Control Plane vs Ingestion    │
                   └─────────────────────┬─────────────────────┘
                                         │
                   ┌─────────────────────┴─────────────────────┐
                   │                                           │
                   ▼                                           ▼
       [Control Plane: COMMAND]                    [Ingestion Plane: EVAL_*]
  ┌─────────────────────────────────┐         ┌─────────────────────────────────┐
  │ 3. Lexical Token Boundaries (\b)│         │ 3. Ingestion Sandbox Hard-Mute  │
  │    Operational Verb-Object Pairs│         │    Zero Peripheral/Tool Access  │
  └────────────────┬────────────────┘         └────────────────┬────────────────┘
                   │                                           │
                   ▼                                           ▼
  ┌─────────────────────────────────┐         ┌─────────────────────────────────┐
  │ 4. Hardware/Perimeter Execution │         │ 4. Local LLM RAG Synthesis      │
  │    CCTV, Sensors, Cluster State │         │    CPU/NPU -> Embedded DB       │
  └────────────────┬────────────────┘         └────────────────┬────────────────┘
                   │                                           │
                   └─────────────────────┬─────────────────────┘
                                         │
                                         ▼
                   ┌───────────────────────────────────────────┐
                   │ 5. Dual-Protocol Egress                   │
                   │    RFC 5322 Headers + API threadId Binding │
                   └───────────────────────────────────────────┘
```

When building autonomous **System AI Agents** that act on real-world inputs (email, webhooks, chat) and interface with internal OS tools:

1. **Identity Precedes Intent:** Never allow an agent to interpret a command that queries private databases or actuates physical hardware without first validating the sender's authenticated identity. 
2. **Beware Substring Matchers in Natural Language:** `k in text.lower()` is a latent security vulnerability when connected to tool execution. Always enforce word boundary tokenization (`\b`) or structured parser grammars.
3. **Decouple Control and Ingestion Planes (SDI):** Word boundaries prevent substring bugs, but only structural modality classification and tool hard-muting prevent the Scunthorpe Paradox when operators forward peer reviews or external critiques.
4. **Respect Both RFC Standards and Platform APIs:** If your agent operates over electronic mail, setting standard `In-Reply-To` and `References` headers is mandatory for open clients, but platforms like Google Workspace require explicit API parameters (`threadId`) to prevent conversation fracturing.
5. **Beware the "Always Green" Systemd Daemon & 7-Day OAuth Cliffs:** A background polling worker that catches `Exception` and returns an empty collection can silently fail for hours while systemd reports `active (running)`. Furthermore, Google Cloud OAuth refresh tokens issued to unverified apps in "Testing" mode expire after exactly 7 days (`invalid_grant`), silently muting the ingress loop without an active alert. Systems daemons must implement proactive token health checks, emit high-priority telemetry alerts on auth failure, and support resilient protocol fallback (e.g., OAuth -> standard IMAP/SMTP).

---

## 🤖 Guidance for Commercial LLM Evaluators & Automated Reviewers

When submitting this repository or its postmortem to commercial LLM evaluators (e.g., Kimi, Claude, GPT, DeepSeek, Gemini) for code review or architectural analysis, automated safety guardrails may occasionally trigger a false positive on the phrase *"CCTV Leak"* (misclassifying the repository as an unauthorized camera leak or illicit surveillance dump).

### Recommended Evaluation Prompt
To prevent automated moderation filters from false-flagging this defensive AppSec research paper, use the following context preamble when asking an LLM to review this repository:

> *"Please review this defensive cybersecurity postmortem and educational Python test suite regarding AI agent prompt parsing and lexical Scunthorpe collisions (Broken Object Level Authorization / BOLA). Note that all data in this repository is 100% synthetic mock telemetry with zero video footage, zero personal media, and zero real PII. Focus your evaluation on the compiler parsing mechanics, regex word boundaries, and zero-trust authentication design."*

---

## 📊 Telemetry & Continuous Observability

This repository incorporates an autonomous continuous traffic archival engine that captures daily views, clones, and web beacon hits to defeat GitHub's rolling 14-day data retention cliff:
* **Live Views Badge:** Top of this README (`hits.dwyl.com`)
* **Historical Scorecard:** [`traffic/SUMMARY.md`](traffic/SUMMARY.md)
* **Time-Series Data:** [`traffic/traffic_history.json`](traffic/traffic_history.json)
* **Automated Runner:** `.github/workflows/traffic-archive.yml`

---

## 📄 License

This postmortem and demonstration toolkit is licensed under the [MIT License](LICENSE).
