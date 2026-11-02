"""PostToolUseFailure hook: when the sonar agent hits the same tool error twice
in one session, tell it to consult the advisor before changing approach
(moment 2 in SKILL.md "Konsultasi advisor").

Only acts in the main thread of `claude --agent sonar-core:sonar`; every other
session and every subagent gets no output. Run with --selftest to check it.
"""
import hashlib
import json
import os
import re
import sys
import tempfile

AGENT = "sonar"  # matches "sonar" and "sonar-core:sonar", not "sonar-scout"

MESSAGE = (
    "SONAR momen 2: tool {tool} gagal dengan error yang sama untuk kedua kalinya "
    "({err}). Sesuai SKILL.md bagian \"Konsultasi advisor\", panggilan tool "
    "berikutnya harus advisor, sebelum ganti cara, ganti jalur, atau menyerah. "
    "Kalau tool advisor tidak tersedia, tulis alasan ganti cara di laporan."
)


def error_key(tool, error):
    """Same tool + same last meaningful error line, numbers ignored."""
    lines = [l.strip() for l in (error or "").splitlines() if l.strip()]
    last = lines[-1] if lines else ""
    return tool + "|" + re.sub(r"\d+", "#", last)[:200], last[:120]


def is_sonar_main(data):
    agent = (data.get("agent_type") or "").split(":")[-1]
    return agent == AGENT and not data.get("agent_id")


def handle(data, state_dir):
    """Return the hook's JSON output, or None for no output."""
    if not is_sonar_main(data) or data.get("is_interrupt"):
        return None
    key, shown = error_key(data.get("tool_name", ""), data.get("error", ""))
    session = re.sub(r"[^\w-]", "", data.get("session_id", "nosession"))
    path = os.path.join(state_dir, "sonar-errors-" + session + ".json")
    try:
        with open(path, encoding="utf-8") as f:
            counts = json.load(f)
    except (OSError, ValueError):
        counts = {}
    h = hashlib.sha1(key.encode("utf-8")).hexdigest()
    counts[h] = counts.get(h, 0) + 1
    os.makedirs(state_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(counts, f)
    if counts[h] != 2:  # nudge once per error kind, on the second hit
        return None
    return {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUseFailure",
            "additionalContext": MESSAGE.format(tool=data.get("tool_name"), err=shown),
        }
    }


def selftest():
    d = tempfile.mkdtemp()
    base = {"session_id": "s1", "agent_type": "sonar-core:sonar", "tool_name": "Bash",
            "error": "Exit code 6\ncurl: (6) Could not resolve host: a.com"}
    assert handle(base, d) is None
    out = handle(dict(base, error="Exit code 6\ncurl: (6) Could not resolve host: b.com"), d)
    assert out is None, "different host text is a different error"
    out = handle(base, d)
    assert out and "momen 2" in out["hookSpecificOutput"]["additionalContext"]
    assert handle(base, d) is None, "only nudge once"
    assert handle(dict(base, agent_type="sonar-core:sonar-scout"), d) is None
    assert handle(dict(base, agent_id="x"), d) is None
    assert handle(dict(base, agent_type=None), d) is None
    assert handle(dict(base, is_interrupt=True), d) is None
    print("selftest ok")


def main():
    if "--selftest" in sys.argv:
        return selftest()
    try:
        data = json.load(sys.stdin)
        state = os.environ.get("CLAUDE_PLUGIN_DATA") or os.path.join(tempfile.gettempdir(), "sonar-core")
        out = handle(data, state)
    except Exception:
        return  # a broken hook must never block the session
    if out:
        print(json.dumps(out))


if __name__ == "__main__":
    main()
