#!/usr/bin/env python3
"""
Example 01: Vulnerable Substring Intent Parser (The 2026 Scunthorpe Collision)
-------------------------------------------------------------------------------
Demonstrates how naive substring containment (`k in text.lower()`) mistakenly
matches character sequences inside unrelated words (e.g. 'log' inside 'biotechnologies'),
leading to intent hijacking and unauthorized database queries.

Run:
    python3 01_vulnerable_parser.py
"""

import sys

# The naive keyword list from the unhardened mail daemon
VISITOR_KEYWORDS = [
    "visitor", "visitors", "doorstep", "front porch", "who came",
    "cctv", "camera", "perimeter", "motion", "log", "summary"
]


def mock_query_camera_database():
    """Simulates querying PostgreSQL for perimeter detections."""
    return (
        "🚨 [CCTV AUDIT EXECUTED]\n"
        "Perimeter Detections:\n"
        "  - [14:22:10] Person detected (Porch CCTV)\n"
        "  - [16:05:44] Person detected (Driveway CCTV)"
    )


def mock_execute_web_research(url):
    """Simulates triggering LLM web research and synthesis."""
    return f"🧠 [RESEARCH ENGINE EXECUTED] Synthesizing brief for: {url}"


def parse_and_route_vulnerable(subject: str, body: str):
    """Vulnerable routing logic using naive substring matching."""
    full_text = f"{subject} {body}".lower()
    
    print(f"\n📨 Inbound Email:")
    print(f"   Subject: {subject}")
    print(f"   Body:    {body}")

    # DEFECT: Substring containment check
    matched_keyword = None
    for kw in VISITOR_KEYWORDS:
        if kw in full_text:
            matched_keyword = kw
            break

    if matched_keyword:
        print(f"   ⚠️ MISCLASSIFIED! Substring match found: '{matched_keyword}' in text!")
        return mock_query_camera_database()
    elif "http://" in full_text or "https://" in full_text:
        return mock_execute_web_research(body.strip())
    else:
        return "ℹ️ [DEFAULT] General assistant query."


def main():
    print("=" * 70)
    print("🧪 SIMULATING VULNERABLE SUBSTRING INTENT PARSER")
    print("=" * 70)

    # Test Case 1: Legitimate Visitor Request
    res1 = parse_and_route_vulnerable(
        subject="Check doorstep",
        body="Can you show me who came to the front door today?"
    )
    print(f"   Output:\n{res1}\n")

    # Test Case 2: The Biotechnology Paper (Accidental Collision!)
    res2 = parse_and_route_vulnerable(
        subject="199-biotechnologies/claude-deep-research-skill",
        body="Please assess this framework for usability: https://github.com/example/repo"
    )
    print(f"   Output:\n{res2}\n")

    # Test Case 3: Another classical Scunthorpe trap: "prologue" contains "log"
    res3 = parse_and_route_vulnerable(
        subject="Review the research prologue",
        body="Link: https://example.com/prologue"
    )
    print(f"   Output:\n{res3}\n")


if __name__ == "__main__":
    main()
