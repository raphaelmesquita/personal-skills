#!/usr/bin/env python3
import json
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

API_URL = "https://chatgpt.com/backend-api/wham/rate-limit-reset-credits"
AUTH_PATH = Path.home() / ".codex" / "auth.json"
TIMEZONE = "America/Sao_Paulo"


def fmt(timestamp):
    if not timestamp:
        return "not set"
    parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    return parsed.astimezone(ZoneInfo(TIMEZONE)).strftime("%Y-%m-%d %I:%M:%S %p %Z")


def fmt_expiry_terminal(timestamp):
    if not timestamp:
        return "not set"
    parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    now = datetime.now(parsed.tzinfo)
    time_left = parsed - now
    
    formatted = parsed.astimezone(ZoneInfo(TIMEZONE)).strftime("%Y-%m-%d %I:%M:%S %p %Z")
    
    # Check if expiring soon (less than 25 days) and active
    days_threshold = 25
    if 0 <= time_left.total_seconds() < days_threshold * 24 * 60 * 60:
        return f"\033[1;31m{formatted} [EXPIRING SOON]\033[0m"
    return formatted


def main():
    auth = json.loads(AUTH_PATH.read_text())
    tokens = auth["tokens"]

    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "OpenAI-Beta": "codex-1",
        "originator": "Codex Desktop",
    }

    account_id = tokens.get("account_id")
    if account_id:
        headers["ChatGPT-Account-ID"] = account_id

    request = urllib.request.Request(API_URL, headers=headers)
    payload = json.loads(urllib.request.urlopen(request, timeout=30).read().decode())
    credits = payload.get("credits") or []

    print(f"1. resets available: {payload.get('available_count', 0)}")
    print("2. granted: " + ("; ".join(fmt(c.get("granted_at")) for c in credits) or "none"))
    print("3. expires: " + ("; ".join(fmt_expiry_terminal(c.get("expires_at")) for c in credits) or "none"))
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()