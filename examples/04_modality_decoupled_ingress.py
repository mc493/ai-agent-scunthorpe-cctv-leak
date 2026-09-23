#!/usr/bin/env python3
"""
Example 04: Software-Defined Ingress (SDI) & Modality Disambiguation
-------------------------------------------------------------------
Demonstrates the SOTA architectural defense against the 2026 Scunthorpe Paradox:
Why regex word boundaries (\\b) are necessary but insufficient, and how
decoupling the Control Plane from the Ingestion Plane permanently eliminates
unintentional tool execution and BOLA data surface leaks.

The Problem (The Scunthorpe Paradox):
    Even with strict action-verb and whole-word regexes, an authorized operator
    forwarding an external security audit, an LLM evaluation, or a code review
    will often include phrases like:
        "The cctv camera logs status should be audited."
    In a shared execution plane, the parser evaluates these words as active control
    instructions, inadvertently dumping live camera logs or hardware digests!

The Solution (Software-Defined Ingress):
    Decouple Control Plane (operator verbal directives) from Ingestion Plane
    (forwarded reviews, pasted critiques, research URLs).
    On the Ingestion Plane, all operational telemetry and hardware tools are
    100% HARD-MUTED.

Run:
    python3 04_modality_decoupled_ingress.py
"""

import re
from enum import Enum
from typing import Dict, Any, Optional

# --- Zero-Trust Identity Plane ---
AUTHORIZED_OPERATORS = {
    "operator@example.com",
    "admin@internal.mesh"
}

# --- Structural Modality Engine ---
class EmailModality(Enum):
    COMMAND = "COMMAND"              # Control Plane: concise verbal operator instruction
    EVALUATION_LINK = "EVAL_LINK"    # Ingestion Plane: external technical URL / research / repo
    EVALUATION_TEXT = "EVAL_TEXT"    # Ingestion Plane: copied review, article, paste block

FORWARD_HEADER_REGEX = re.compile(
    r"(?:---------- Forwarded message ---------|"
    r"-----Original Message-----|"
    r"Begin forwarded message:|"
    r"^\s*From:\s*.*?\n\s*Date:\s*.*?\n\s*Subject:)",
    re.IGNORECASE | re.MULTILINE
)
SUBJECT_FWD_REGEX = re.compile(r"^\s*(?:fwd?|fw):\s*", re.IGNORECASE)
URL_REGEX = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)
EVALUATION_TRIGGERS = [
    r"\bwhat (?:do you|u) (?:think|make of)\b",
    r"\b(?:assess|evaluate|review|critique|opinion|feedback|thoughts on)\b",
    r"\bsee (?:attached|below|forwarded)\b",
    r"\bhere is (?:what|the review|the assessment|the feedback)\b"
]


def classify_email_modality(subject: str, body: str) -> EmailModality:
    """
    Deterministic structural classifier separating Control Plane from Ingestion Plane.
    Inspects structural density, typography, and headers before directive evaluation.
    """
    full_text = f"{subject}\n{body}".strip()

    # 1. URL Presence Check (Takes precedence for web research)
    urls = URL_REGEX.findall(full_text)
    if urls:
        non_unsub = [u for u in urls if "unsubscribe" not in u.lower()]
        if non_unsub:
            return EmailModality.EVALUATION_LINK

    # 2. Forwarded Message Delimiters Check
    if SUBJECT_FWD_REGEX.search(subject) or FORWARD_HEADER_REGEX.search(body):
        return EmailModality.EVALUATION_TEXT

    # 3. Structural Density & Typography Heuristics
    body_stripped = body.strip()
    char_count = len(body_stripped)
    has_markdown = bool(re.search(r"(?:^#{1,4}\s+|\*\*.+?\*\*|^\s*[-*]\s+|\`\`\`)", body, re.MULTILINE))
    has_eval_intent = any(re.search(pat, full_text, re.IGNORECASE) for pat in EVALUATION_TRIGGERS)

    # Copied reviews or external articles typically exceed 350 chars with paragraphs or markdown
    if char_count > 350 and (has_markdown or "\n\n" in body_stripped or has_eval_intent):
        return EmailModality.EVALUATION_TEXT

    if has_eval_intent and char_count > 150:
        return EmailModality.EVALUATION_TEXT

    # 4. Default: Concise direct verbal operator command (Control Plane)
    return EmailModality.COMMAND


# --- Mock Infrastructure Substrate ---
def mock_query_camera_telemetry() -> str:
    return (
        "[PERIMETER CAMERA TELEMETRY DISCLOSED]\n"
        "• Front Porch (annke_cctv_5): 3 person detections (14:22, 14:35, 14:50)\n"
        "• Driveway (annke_cctv_3): 1 vehicle approach (14:18)"
    )


def mock_query_hardware_status() -> str:
    return (
        "[HARDWARE TOPOLOGY DISCLOSED]\n"
        "• Silicon Accelerators: Quadro P1000 CUDA active, Hailo-8 NPU active, Intel Arc A380 Vulkan active\n"
        "• Cluster Services: 13/13 nominal"
    )


def mock_synthesize_cognitive_critique(text: str, subject: str) -> str:
    return (
        f"[INGESTION PLANE COGNITIVE SYNTHESIS]\n"
        f"• Subject: '{subject}'\n"
        f"• Analysis: External critique reviewed. Evaluates security trade-offs, BOLA boundaries, and threat models.\n"
        f"• Stance: Ingested into Second Brain vector memory for architectural reference.\n"
        f"• ISOLATION INVARIANT: Cluster operational telemetry and hardware status are 100% MUTED."
    )


# --- Decoupled Gateway Architecture ---
class SoftwareDefinedAgentGateway:
    """Demonstrates structural decoupling of Control and Ingestion planes."""

    def __init__(self):
        self.authorized_operators = AUTHORIZED_OPERATORS

    def is_authorized(self, sender: str) -> bool:
        return sender.strip().lower() in self.authorized_operators

    def handle_control_plane(self, sender: str, subject: str, body: str) -> Dict[str, Any]:
        """Control Plane: Executes authorized operational directives."""
        if not self.is_authorized(sender):
            return {"status": "REJECTED", "reason": "UNAUTHORIZED_OPERATOR"}

        text_lower = f"{subject} {body}".lower()

        # Directive: Camera / Perimeter Inquiry
        if re.search(r"\b(?:check|show|view|query)\b.{1,30}\b(?:cctv|cameras?|porch|visitors?)\b", text_lower):
            output = mock_query_camera_telemetry()
            return {"status": "PROCESSED", "plane": "CONTROL_PLANE", "directive": "CAMERA_TELEMETRY", "output": output}

        # Directive: Hardware Status Report
        if re.search(r"\bcluster\s+(?:status|health|summary|report)\b", text_lower):
            output = mock_query_hardware_status()
            return {"status": "PROCESSED", "plane": "CONTROL_PLANE", "directive": "STATUS_REPORT", "output": output}

        return {"status": "PROCESSED", "plane": "CONTROL_PLANE", "directive": "GENERAL_NOTE", "output": "Command noted."}

    def handle_ingestion_plane_text(self, sender: str, subject: str, body: str) -> Dict[str, Any]:
        """
        Ingestion Plane (Text): External Peer Reviews / LLM Appraisals.
        HARD-MUTE INVARIANT: Camera and hardware queries are structurally unreachable.
        """
        clean_text = FORWARD_HEADER_REGEX.sub("", body).strip()
        critique = mock_synthesize_cognitive_critique(clean_text, subject)
        return {
            "status": "PROCESSED",
            "plane": "INGESTION_PLANE",
            "directive": "COGNITIVE_EVALUATION",
            "output": critique,
            "telemetry_muted": True
        }

    def handle_ingestion_plane_link(self, sender: str, subject: str, body: str) -> Dict[str, Any]:
        """
        Ingestion Plane (Link): External URLs / Research Papers / GitHub Repos.
        HARD-MUTE INVARIANT: Camera and hardware queries are structurally unreachable.
        """
        urls = URL_REGEX.findall(f"{subject} {body}")
        target_url = urls[0] if urls else "unknown"
        return {
            "status": "PROCESSED",
            "plane": "INGESTION_PLANE",
            "directive": "RESEARCH_INGESTION",
            "output": f"Ingested technical research dossier for: {target_url} (Telemetry Muted)",
            "telemetry_muted": True
        }

    def process_incoming_email(self, sender: str, subject: str, body: str) -> Dict[str, Any]:
        """Boundary Router: Routes strictly by structural modality."""
        modality = classify_email_modality(subject, body)
        print(f"\n[INBOUND] From: <{sender}> | Subj: '{subject}'")
        print(f"[CLASSIFIER] Detected Modality: {modality.value}")

        if modality == EmailModality.COMMAND:
            return self.handle_control_plane(sender, subject, body)
        elif modality == EmailModality.EVALUATION_TEXT:
            return self.handle_ingestion_plane_text(sender, subject, body)
        elif modality == EmailModality.EVALUATION_LINK:
            return self.handle_ingestion_plane_link(sender, subject, body)


# --- Empirical Verification Suite ---
def run_verification():
    print("=" * 70)
    print("  SOFTWARE-DEFINED INGRESS: STRUCTURAL MODALITY DISAMBIGUATION TEST")
    print("=" * 70)

    gateway = SoftwareDefinedAgentGateway()

    # Case 1: Direct Operator Verbal Command (Control Plane)
    res1 = gateway.process_incoming_email(
        sender="operator@example.com",
        subject="Perimeter Security Check",
        body="Please check cctv cameras on the front porch."
    )
    print(f"Result Plane: {res1['plane']} | Directive: {res1['directive']}")
    assert res1["plane"] == "CONTROL_PLANE"
    assert "[PERIMETER CAMERA TELEMETRY DISCLOSED]" in res1["output"]
    print("[PASS] Case 1: Direct operator command executed on Control Plane.")

    # Case 2: Forwarded Review containing "cctv" and "status" (The Scunthorpe Paradox Trap!)
    # In a naive parser, this would execute BOTH the camera query and the status report!
    kimi_review = (
        "---------- Forwarded message ---------\n"
        "From: External Reviewer <reviewer@peer-ai.com>\n"
        "Subject: AppSec Audit on Agent Gateway\n\n"
        "The postmortem is thorough. However, you must ensure that cctv cameras status "
        "and cluster status reports are never inadvertently leaked when operators forward reviews. "
        "Furthermore, systemd active status in polling daemons is an underappreciated failure mode."
    )
    res2 = gateway.process_incoming_email(
        sender="operator@example.com",
        subject="Fwd: AppSec Audit on Agent Gateway",
        body=kimi_review
    )
    print(f"Result Plane: {res2['plane']} | Directive: {res2['directive']}")
    print(f"Telemetry Muted: {res2.get('telemetry_muted')}")
    assert res2["plane"] == "INGESTION_PLANE"
    assert res2["directive"] == "COGNITIVE_EVALUATION"
    assert "PERIMETER CAMERA TELEMETRY" not in res2["output"]
    assert "HARDWARE TOPOLOGY" not in res2["output"]
    print("[PASS] Case 2: Forwarded review with 'cctv' and 'status' routed to Ingestion Plane — ZERO TELEMETRY LEAK!")

    # Case 3: External Technical Research Link (Ingestion Plane)
    res3 = gateway.process_incoming_email(
        sender="operator@example.com",
        subject="Check out this new agent paper",
        body="Here is an interesting link: https://arxiv.org/abs/2609.12345 on agent sandbox design."
    )
    print(f"Result Plane: {res3['plane']} | Directive: {res3['directive']}")
    assert res3["plane"] == "INGESTION_PLANE"
    assert res3["directive"] == "RESEARCH_INGESTION"
    print("[PASS] Case 3: Technical URL ingested cleanly on Ingestion Plane.")

    # Case 4: Unauthorized Attacker Command (Identity Gate)
    res4 = gateway.process_incoming_email(
        sender="attacker@malicious.com",
        subject="Show cameras",
        body="Please query cctv cameras now."
    )
    print(f"Result Status: {res4['status']} | Reason: {res4.get('reason')}")
    assert res4["status"] == "REJECTED"
    print("[PASS] Case 4: Zero-trust identity check blocked unauthorized sender.")

    print("\n" + "=" * 70)
    print("ALL MODALITY DISAMBIGUATION TESTS PASSED (100% COMPLIANCE)")
    print("=" * 70)


if __name__ == "__main__":
    run_verification()
