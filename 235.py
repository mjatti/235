#!/usr/bin/env python3
import requests
import base64
import tempfile
import subprocess
import sys
import tty
import termios
import select
import re

def fetch_image(page: str, subpage: str):
    url = f"https://yle.fi/aihe/yle-ttv/json?P={page}_{subpage}"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        img_field = resp.json()["data"][0]["content"]["image"]
        b64 = img_field.split("base64,")[1].split('"')[0]
        return base64.b64decode(b64)
    except Exception:
        return None

def render_image(image_bytes):
    # Tallenna kursorin paikka
    print("\033[s", end="", flush=True)

    # Piirrä kuva heti nykyisen rivin alle
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(image_bytes)
        tmp.flush()
        subprocess.run([
            "chafa",
            "--fill=space",
            "--symbols=block",
            "--clear",  # korvaa edellisen kuvan alueen
            tmp.name
        ], stdout=sys.stdout, stderr=subprocess.DEVNULL)

    # Palauta kursori komentoriville
    print("\033[u", end="", flush=True)
    sys.stdout.flush()

def read_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        if select.select([sys.stdin], [], [], 0.5)[0]:
            return sys.stdin.read(1)
        else:
            return ''
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def main():
    print("Teksti-TV-selain (q lopettaa)")
    page = "100"
    subpage = "0001"
    buffer = ""

    img = fetch_image(page, subpage)
    if img:
        render_image(img)

    while True:
        ch = read_key()
        if not ch:
            continue
        if ch == "q":
            print("\nPoistutaan.")
            break
        if ch in "0123456789":
            buffer += ch
            if len(buffer) == 3:
                page = buffer
                subpage = "0001"
                img = fetch_image(page, subpage)
                if img:
                    render_image(img)
                buffer = ""
        elif ch == ".":
            buffer += "."
        elif ch in "0123456789" and buffer.endswith("."):
            buffer += ch
            match = re.fullmatch(r"(\d{3})\.(\d)", buffer)
            if match:
                page = match.group(1)
                subpage = f"000{match.group(2)}"
                img = fetch_image(page, subpage)
                if img:
                    render_image(img)
                buffer = ""
        elif ch in "vmbn":
            buffer = ""
            if ch == "v":
                page = f"{int(page)-1:03}"
                subpage = "0001"
            elif ch == "m":
                page = f"{int(page)+1:03}"
                subpage = "0001"
            elif ch == "b":
                subpage = f"{max(1, int(subpage)-1):04}"
            elif ch == "n":
                subpage = f"{int(subpage)+1:04}"
            img = fetch_image(page, subpage)
            if img:
                render_image(img)
        else:
            buffer = ""

if __name__ == "__main__":
    main()

