#!/usr/bin/env python3
"""RAM usage monitor — alerts when usage exceeds a threshold."""

import time
import sys
import psutil
from datetime import datetime

THRESHOLD = 80.0   # percent
INTERVAL  = 5      # seconds


def format_bytes(n):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


RESET  = "\033[0m"
BOLD   = "\033[1m"
RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"


def color_for(pct):
    if pct >= THRESHOLD:
        return RED
    if pct >= THRESHOLD * 0.85:
        return YELLOW
    return GREEN


def print_status(mem, alert=False):
    ts  = datetime.now().strftime("%H:%M:%S")
    pct = mem.percent
    col = color_for(pct)

    bar_len   = 30
    filled    = int(bar_len * pct / 100)
    bar       = "█" * filled + "░" * (bar_len - filled)

    prefix = f"{RED}{BOLD}[ALERT]{RESET} " if alert else "       "

    print(
        f"{CYAN}{ts}{RESET} {prefix}"
        f"RAM: {col}{BOLD}{pct:5.1f}%{RESET} "
        f"[{col}{bar}{RESET}] "
        f"used {format_bytes(mem.used)} / {format_bytes(mem.total)}"
    )

    if alert:
        print(
            f"         {RED}Available: {format_bytes(mem.available)}"
            f"  —  {mem.percent:.1f}% exceeds {THRESHOLD:.0f}% threshold{RESET}"
        )


def main():
    print(f"{BOLD}RAM Monitor{RESET}  |  threshold: {THRESHOLD:.0f}%  |  interval: {INTERVAL}s  |  Ctrl-C to stop\n")

    try:
        while True:
            mem   = psutil.virtual_memory()
            alert = mem.percent >= THRESHOLD
            print_status(mem, alert=alert)
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print(f"\n{CYAN}Monitor stopped.{RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()
