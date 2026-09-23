#!/usr/bin/env python3
"""
Example 03: RFC 5322 Compliance & Google Workspace REST API Thread Binding
--------------------------------------------------------------------------
Demonstrates how autonomous email agents must satisfy BOTH standard MIME headers
(RFC 2822 / 5322) and platform-specific API requirements (Google Workspace Bigtable threadId)
to prevent conversational thread severance.

Run:
    python3 03_rfc5322_threading.py
"""

import base64
from email.message import EmailMessage


def build_defective_reply(sender: str, original_subject: str, summary: str):
    """
    Defective builder: Mutates the subject line, omits In-Reply-To/References,
    and sends bare raw bytes to the API.
    """
    msg = EmailMessage()
    msg["To"] = sender
    msg["From"] = "System AI Agent <agent@example.com>"
    msg["Subject"] = f"Research Synthesis: New Topic"  # Breaks subject heuristic!
    msg.set_content(summary)

    raw_bytes = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    
    # DEFECT: Missing threadId in outer dictionary
    api_payload = {
        "raw": raw_bytes
        # ❌ Missing: "threadId": thread_id
    }
    return msg, api_payload


def build_hardened_reply(sender: str, original_subject: str, message_id: str, thread_id: str, summary: str):
    """
    Hardened builder:
      1. Preserves RFC 5322 headers (In-Reply-To, References, Re: Subject)
      2. Injects Bigtable threadId into the Google Workspace REST API JSON body
    """
    msg = EmailMessage()
    msg["To"] = sender
    msg["From"] = "System AI Agent <agent@example.com>"
    
    # Standardize Subject:
    if original_subject.lower().startswith("re:"):
        msg["Subject"] = original_subject
    else:
        msg["Subject"] = f"Re: {original_subject}"

    # RFC 5322 In-Thread Anchors:
    if message_id:
        msg["In-Reply-To"] = message_id
        msg["References"] = message_id

    msg.set_content(summary)

    raw_bytes = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    
    # GOOGLE WORKSPACE API BINDING:
    api_payload = {"raw": raw_bytes}
    if thread_id:
        api_payload["threadId"] = thread_id

    return msg, api_payload


def main():
    print("=" * 70)
    print("📧 SIMULATING DUAL-PROTOCOL EMAIL THREAD CONSTRUCTOR")
    print("=" * 70)

    inbound_meta = {
        "sender": "operator@example.com",
        "subject": "199-biotechnologies/claude-deep-research-skill",
        "message_id": "<CADx123_abc@mail.gmail.com>",
        "thread_id": "18e4f8a92bc4412e"  # Bigtable Thread Key
    }

    print(f"\n📩 Inbound Message Ingested:")
    print(f"   Subject:    {inbound_meta['subject']}")
    print(f"   Message-ID: {inbound_meta['message_id']}")
    print(f"   Thread-ID:  {inbound_meta['thread_id']}")

    # 1. Defective Reply
    def_msg, def_payload = build_defective_reply(
        sender=inbound_meta["sender"],
        original_subject=inbound_meta["subject"],
        summary="Executive Brief on Deep Research Skill..."
    )
    print("\n❌ 1. DEFECTIVE OUTBOUND DISPATCH:")
    print(f"   MIME Subject:      '{def_msg['Subject']}'")
    print(f"   MIME In-Reply-To:  {def_msg.get('In-Reply-To')}")
    print(f"   MIME References:   {def_msg.get('References')}")
    print(f"   API Payload Keys:  {list(def_payload.keys())}")
    print("   -> RESULT: Fractures conversation! Gmail creates a detached thread.")

    # 2. Hardened Reply
    hard_msg, hard_payload = build_hardened_reply(
        sender=inbound_meta["sender"],
        original_subject=inbound_meta["subject"],
        message_id=inbound_meta["message_id"],
        thread_id=inbound_meta["thread_id"],
        summary="Executive Brief on Deep Research Skill..."
    )
    print("\n✅ 2. HARDENED OUTBOUND DISPATCH:")
    print(f"   MIME Subject:      '{hard_msg['Subject']}'")
    print(f"   MIME In-Reply-To:  {hard_msg.get('In-Reply-To')}")
    print(f"   MIME References:   {hard_msg.get('References')}")
    print(f"   API Payload Keys:  {list(hard_payload.keys())}")
    print(f"   API Thread ID:     '{hard_payload.get('threadId')}'")
    print("   -> RESULT: Seamless threading across all web, desktop, and mobile MUAs!")


if __name__ == "__main__":
    main()
