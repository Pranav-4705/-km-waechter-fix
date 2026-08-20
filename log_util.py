"""Lightweight logger that writes to stdout and a buffer for flushing to disk."""

import time

LOG_LINES: list[str] = []


def log(message: str) -> None:
    """Append a timestamped line to the in-memory log and stdout."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def flush_log(path: str) -> None:
    """Append all buffered log lines to *path* and clear the buffer."""
    with open(path, "a") as f:
        for line in LOG_LINES:
            f.write(line + "\n")
    LOG_LINES.clear()
