# How a "Biotechnology" Link Made a System AI Agent Leak Home CCTV Logs
*A Postmortem on Lexical Collisions, System-Level Agent Authorization, and the 2026 Scunthorpe Problem*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Views](https://hits.dwyl.com/mc493/ai-agent-scunthorpe-cctv-leak.svg?style=flat-square&label=views)](traffic/SUMMARY.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/mc493/ai-agent-scunthorpe-cctv-leak/pulls)

---

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
```

---

## 🔍 The Mystery: A GitHub Link Triggers a Perimeter Security Audit

Yesterday evening, I emailed a GitHub link to my self-hosted **System AI Agent**. The link pointed to `claude-deep-research-skill`, an open-source deep research framework developed by 199-biotechnologies (a UK longevity biotech lab). The email was simple:

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

The System AI Agent had queried my internal PostgreSQL computer-vision database, aggregated 24 hours of real-time person detections from my outdoor cameras, and dispatched my household physical presence schedule via email.

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

1. **Token-Boundary Parsing (`\b`):** All lexical intent keywords were migrated to strict regex word boundaries and structured multi-token phrases:
   ```python
   visitor_patterns = [
       r"\bvisitors?\b", r"\bvisited\b", r"\bcctv\b",
       r"\bsecurity (?:log|audit|check)\b", r"\bvisitor (?:log|audit|history)\b"
   ]
   ```
   Now, `"biotechnologies"` cannot trigger `"log"`, nor can `"dialogue"`, `"prologue"`, or `"catalog"`.

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

## 5. Architectural Summary & Lessons Learned

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
                  │ 2. Defensive Injection Quarantine         │
                  │    Shannon entropy & command blocklists   │
                  └─────────────────────┬─────────────────────┘
                                        │
                                        ▼
                  ┌───────────────────────────────────────────┐
                  │ 3. Lexical Token Boundaries (\b)          │
                  │    Strict Priority: URLs -> Sensor Queries │
                  └─────────────────────┬─────────────────────┘
                                        │
                                        ▼
                  ┌───────────────────────────────────────────┐
                  │ 4. Execution & Synthesis                  │
                  │    Local LLM on CPU/NPU -> Embedded DB    │
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
3. **Respect Both RFC Standards and Platform APIs:** If your agent operates over electronic mail, setting standard `In-Reply-To` and `References` headers is mandatory for open clients, but platforms like Google Workspace require explicit API parameters (`threadId`) to prevent conversation fracturing.
4. **Beware the "Always Green" Systemd Daemon:** A background polling worker that catches `Exception` and returns an empty collection can silently fail for hours while systemd reports `active (running)`. Continuous synthetic end-to-end integration tests (asserting that an unread message actually transitions to processed state) are essential for autonomous daemons.

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
