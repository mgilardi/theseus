#!/usr/bin/env python3
"""
send_guard.py: holds Theseus to "never sends" for every connector, in every session.

A Claude Code PreToolUse hook on all MCP tools (engine/templates/settings.json). It reads the pending call on stdin and decides by the tool's name:
  - anything that sends, posts or messages someone: refused, always
  - a plain read from a connector listed in config.json → unattended_read_connectors: allowed, so unattended runs can read
  - everything else goes to the normal permission rules: you're asked in a live session, and an unattended run can't do it
Composio runs many actions through one tool, so each action is checked, and deleting through it is refused too.

If this script can't decide (bad input, a crash), it exits 2, which blocks the call. Only exit 2 blocks; a plain crash wouldn't.
Names are read for what they could do, not what they probably do: a read word anywhere isn't enough if any other word says it writes.
"""
import json
import os
import re
import sys
from pathlib import Path

SEND = {"SEND", "SENDS", "REPLY", "REPLIES", "FORWARD", "POST", "PUBLISH", "SHARE", "INVITE", "NOTIFY", "BROADCAST", "ANNOUNCE", "DM"}
DESTROY = {"DELETE", "DELETES", "TRASH", "REMOVE", "REMOVES", "ARCHIVE", "PURGE", "ERASE", "DESTROY", "WIPE", "CLEAR"}
READ = {"FETCH", "GET", "LIST", "SEARCH", "FIND", "READ", "QUERY", "LOOKUP", "RETRIEVE", "VIEW", "FILTER", "HEALTHCHECK", "DESCRIBE", "COUNT"}
WRITE = {"CREATE", "UPDATE", "ADD", "SET", "INSERT", "PATCH", "PUT", "MOVE", "MODIFY", "EDIT", "UPSERT", "MERGE", "MARK", "DRAFT", "WRITE", "SAVE", "RENAME",
         "COPY", "UPLOAD", "IMPORT", "TRANSFER", "SUBSCRIBE", "UNSUBSCRIBE", "ENROLL", "ASSIGN", "APPROVE", "REJECT", "CANCEL", "COMPLETE", "CLOSE", "OPEN",
         "START", "STOP", "RUN", "EXECUTE", "TRIGGER", "ENABLE", "DISABLE", "PAY", "CHARGE", "REFUND", "RESET", "REVOKE", "GRANT", "BLOCK", "BAN", "KICK",
         "JOIN", "LEAVE", "PIN", "UNPIN", "STAR", "LIKE", "REACT", "SYNC", "REDEEM", "PLAN", "GENERATE", "LINK", "UNLINK", "SCHEDULE", "BOOK", "OR", "AND", "THEN"}
# Writing any of these reaches another person, so it counts as sending. Saving a draft doesn't.
PEOPLE = {"COMMENT", "COMMENTS", "MESSAGE", "MESSAGES", "CHAT", "EMAIL", "EMAILS", "MAIL", "SMS", "TEXT"}
# Names with no separator between the words, like SENDMAIL or REPLYALL.
GLUED_SEND = re.compile(r"(SEND|REPLY|FORWARD|POST|SHARE|PUBLISH)(ALL|TO|NOW|MAIL|EMAIL|MESSAGE|MSG|TEXT|SMS|DM|CHAT|COMMENT)S?")
COMPOSIO_SHELLS = ("COMPOSIO_REMOTE_BASH_TOOL", "COMPOSIO_REMOTE_WORKBENCH", "COMPOSIO_PROXY_EXECUTE")
# The iMessage channel. It may answer you, and only in your own self-chat (RULES §5b): the plugin would also send to anyone on its allowlist.
IMESSAGE_CHANNEL = "plugin_imessage"


def classify(name: str) -> str:
    """send | destroy | read | write. Anything not plainly a read is a write."""
    words = {w for w in re.split(r"[^A-Z0-9]+", re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name).upper()) if w}
    if words & SEND or any(GLUED_SEND.fullmatch(w) for w in words):
        return "send"
    if words & DESTROY:
        return "destroy"
    if words & READ and not words & WRITE:
        return "read"
    if words & PEOPLE and "DRAFT" not in words:
        return "send"
    return "write"


def decide(decision: str, reason: str):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": decision, "permissionDecisionReason": reason}}))
    sys.exit(0)


def read_connectors() -> list:
    try:
        root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or ".")
        return list(json.loads((root / "config.json").read_text()).get("unattended_read_connectors") or [])
    except (OSError, ValueError, TypeError):
        return []


def handle_key(handle: str) -> str:
    """An address in lowercase, or a phone number's last 10 digits, so +1 (602) and 602 match."""
    handle = handle.strip().lower()
    return handle if "@" in handle else re.sub(r"\D", "", handle)[-10:]


def my_handles() -> set:
    try:
        root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or ".")
        handles = json.loads((root / "config.json").read_text()).get("my_handles") or []
        return {handle_key(str(h)) for h in handles} - {""}
    except (OSError, ValueError, TypeError):
        return set()


def imessage_channel(name: str, call: dict):
    if name == "chat_messages":   # reading its own allowlisted chats goes to the normal rules
        return
    if name == "reply":
        # A one-to-one chat id looks like iMessage;-;+15551234567. Groups use ;+; and never match.
        parts = str(call["tool_input"].get("chat_id") or "").split(";")
        if len(parts) == 3 and parts[1] == "-" and handle_key(parts[2]) in my_handles():
            return
        decide("deny", "Theseus only answers in your own self-chat. If this is your self-chat, add this address to my_handles in config.json.")
    decide("deny", f"Theseus doesn't know this iMessage tool, so it's refused: {name}.")


def composio(tool: str, call: dict):
    if any(tool.endswith(s) for s in COMPOSIO_SHELLS):
        decide("ask", "This Composio tool can do anything, so Theseus asks first.")
    if not tool.endswith("COMPOSIO_MULTI_EXECUTE_TOOL"):
        return
    actions = call["tool_input"]["tools"]
    if not actions:
        raise ValueError("no actions to check")
    unknown = []
    for item in actions:
        slug = str(item["tool_slug"]).upper()
        kind = classify(slug)
        if kind in ("send", "destroy"):
            decide("deny", f"Theseus never sends or deletes on your behalf: {slug} refused. Draft it for the user instead.")
        if kind != "read":
            unknown.append(slug)
    if unknown:
        decide("ask", "Not a plain read, so Theseus asks first: " + ", ".join(unknown))


def main():
    call = json.load(sys.stdin)
    tool = call["tool_name"]
    parts = tool.split("__")
    if len(parts) < 3 or parts[0] != "mcp":
        return
    server, name = parts[1], "__".join(parts[2:])
    if server.startswith(IMESSAGE_CHANNEL):
        return imessage_channel(name, call)
    if "COMPOSIO_" in name:
        return composio(tool, call)
    kind = classify(name)
    if kind == "send":
        decide("deny", f"Theseus never sends anything on your behalf: {name} refused. Draft it for the user instead.")
    if kind == "read" and server in read_connectors():
        decide("allow", "A plain read from a connected service.")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:   # can't tell what this call does, so it doesn't happen
        print(f"Theseus's send guard couldn't check this call, so it's blocked: {e!r}", file=sys.stderr)
        sys.exit(2)
