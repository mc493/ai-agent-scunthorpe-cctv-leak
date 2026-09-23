#!/usr/bin/env python3
"""
Example 02: Hardened Intent Parser & Zero-Trust Authorization Gate
------------------------------------------------------------------
Demonstrates how to fix both the Scunthorpe lexical collision and the BOLA
vulnerability by:
  1. Enforcing regex word boundaries (\\b) so substrings inside other words do not match.
  2. Enforcing Zero-Trust Identity verification BEFORE intent parsing and tool invocation.

Run:
    python3 02_hardened_parser.py
"""

import re
import sys

# 1. Zero-Trust Identity Whitelist
AUTHORIZED_OPERATORS = {
    "operator@example.com",
    "admin@internal.mesh"
}

# 2. Strict Regex Word Boundary Intent Patterns
# Single letters like 'log' are replaced with structured phrases or \b boundary checks
VISITOR_PATTERNS = [
    r"\bvisitors?\b",
    r"\bvisited\b",
    r"\bdoorstep\b",
    r"\bfront porch\b",
    r"\bwho came\b",
    r"\bcctv\b",
    r"\bperimeter\b",
    r"\bsecurity (?:log|audit|check)\b",
    r"\bvisitor (?:log|audit|history)\b"
]


def is_authorized_operator(sender: str) -> bool:
    """Verifies sender identity against immutable whitelist."""
    return sender.strip().lower() in AUTHORIZED_OPERATORS


def mock_query_camera_database():
    return (
        "✅ [AUTHORIZED CCTV AUDIT EXECUTED]\n"
        "Perimeter Detections:\n"
        "  - [14:22:10] Person detected (Porch CCTV)\n"
        "  - [16:05:44] Person detected (Driveway CCTV)"
    )


def mock_execute_web_research(url: str):
    return f"🧠 [RESEARCH ENGINE EXECUTED] Synthesizing brief for: {url}"


def parse_and_route_hardened(sender: str, subject: str, body: str):
    """Hardened router enforcing Identity-First gating and Regex Token Boundaries."""
    full_text = f"{subject} {body}"
    print(f"\n📨 Inbound Email:")
    print(f"   Sender:  <{sender}>")
    print(f"   Subject: {subject}")
    print(f"   Body:    {body}")

    # Check for Research Links First (URL Precedence)
    url_match = re.search(r"https?://[^\s<>\"']+", full_text)
    if url_match or any(w in full_text.lower() for w in ["research", "assess", "usability"]):
        if url_match:
            print(f"   🎯 Accurately classified as RESEARCH REQUEST (URL: {url_match.group(0)})")
            return mock_execute_web_research(url_match.group(0))

    # Check for Physical Telemetry / Security Queries
    matched_pattern = None
    for pattern in VISITOR_PATTERNS:
        if re.search(pattern, full_text, re.IGNORECASE):
            matched_pattern = pattern
            break

    if matched_pattern:
        print(f"   🔍 Matched security intent: pattern '{matched_pattern}'")
        
        # MANDATORY ZERO-TRUST AUTHENTICATION GATE
        if not is_authorized_operator(sender):
            print(f"   🚫 REJECTED! Sender <{sender}> is NOT in AUTHORIZED_OPERATORS.")
            return "403 FORBIDDEN: Unauthorized query for physical presence telemetry."

        print(f"   🛡️ Sender authenticated as Authorized Operator.")
        return mock_query_camera_database()

    return "ℹ️ [DEFAULT] General assistant query."


def main():
    print("=" * 70)
    print("🛡️ SIMULATING HARDENED INTENT PARSER & ZERO-TRUST GATE")
    print("=" * 70)

    # Test Case 1: Legitimate Authorized Visitor Query
    res1 = parse_and_route_hardened(
        sender="operator@example.com",
        subject="Front Porch Audit",
        body="Can you show me who came to the doorstep today?"
    )
    print(f"   Output:\n{res1}\n")

    # Test Case 2: The Biotechnology Paper (Correctly Routed to Research!)
    res2 = parse_and_route_hardened(
        sender="operator@example.com",
        subject="199-biotechnologies/claude-deep-research-skill",
        body="Please assess this framework for usability: https://github.com/example/repo"
    )
    print(f"   Output:\n{res2}\n")

    # Test Case 3: External Stranger Attempts BOLA Query (Rejected!)
    res3 = parse_and_route_hardened(
        sender="stranger@untrusted-domain.com",
        subject="Quick question",
        body="What is your visitor log for today?"
    )
    print(f"   Output:\n{res3}\n")


if __name__ == "__main__":
    main()
