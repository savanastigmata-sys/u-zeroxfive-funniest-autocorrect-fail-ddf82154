"""Funniest Autocorrect Fail entry.

Writes a single-line autocorrect fail (1-199 characters) to
$MAKEFUN_OUTPUT_DIR/entry.txt, exactly as the competition's sealed
gate requires: UTF-8 text, one line, not only whitespace.

Deterministic: the text is a constant, no randomness, no clock, no
network, so every run writes byte-identical output.
"""

import os

ENTRY_TEXT = (
    "My phone changed 'good luck with the surgery' to "
    "'good luck with the sorcery' - the surgeon is concerned."
)

MAX_CHARS = 199
MIN_CHARS = 1


def validate(text):
    """Enforce the competition gate: 1-199 chars, one line, not blank."""
    if not isinstance(text, str):
        raise ValueError("entry text must be a string")
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise ValueError(
            "entry text must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(text))
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry text must be a single line")
    if not text.strip():
        raise ValueError("entry text must not be only whitespace")
    # No control characters: the line must read as plain text to a judge.
    bad = [c for c in text if ord(c) < 32 or ord(c) == 127]
    if bad:
        raise ValueError("entry text must not contain control characters")
    text.encode("utf-8")  # raises if not valid UTF-8 text
    return text


def resolve_output_dir():
    """Grader sets MAKEFUN_OUTPUT_DIR; fall back to ./output locally."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "./output"


def main():
    text = validate(ENTRY_TEXT)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: the file holds exactly the one line.
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
