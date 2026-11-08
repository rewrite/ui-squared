#!/usr/bin/env python3
"""Usage: slop_check.py <file-or-dir> [...]  — flags ui² violations and AI-slop patterns; exits 1 on hits."""
import re
import sys
from pathlib import Path

EXTS = {".html", ".htm", ".css", ".scss", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro"}

CATPPUCCIN = {
    "f5e0dc", "f2cdcd", "f5c2e7", "cba6f7", "f38ba8", "eba0ac", "fab387", "f9e2af", "a6e3a1", "94e2d5",
    "89dceb", "74c7ec", "89b4fa", "b4befe", "cdd6f4", "bac2de", "a6adc8", "9399b2", "7f849c", "6c7086",
    "585b70", "45475a", "313244", "1e1e2e", "181825", "11111b",
    "dc8a78", "dd7878", "ea76cb", "8839ef", "d20f39", "e64553", "fe640b", "df8e1d", "40a02b", "179299",
    "04a5e5", "209fb5", "1e66f5", "7287fd", "4c4f69", "5c5f77", "6c6f85", "7c7f93", "8c8fa1", "9ca0b0",
    "acb0be", "bcc0cc", "ccd0da", "eff1f5", "e6e9ef", "dce0e8",
}

ZERO = r"(?:0|0px|0rem|0em|0%|none)(?:\s*!important)?"

RULES = [
    ("radius", rf"border(?:-[a-z]+)*-radius\s*:(?!\s*{ZERO}\s*[;}}\"'])\s*[^;}}\"']+", "non-zero border-radius"),
    ("radius", r"\brounded(?:-[a-z]{1,3})?-(?!none\b)[\w\[\]/.-]+|\brounded\b(?!-)", "Tailwind rounded-* class"),
    ("gradient", r"(?:linear|radial|conic|repeating-linear|repeating-radial)-gradient\(|\bbg-gradient-|\bbg-linear-|\bfrom-[a-z]+-\d{2,3}\b", "gradient"),
    ("shadow", rf"box-shadow\s*:(?!\s*{ZERO}\s*[;}}\"'])\s*[^;}}\"']+|text-shadow\s*:(?!\s*{ZERO})\s*[^;}}\"']+|drop-shadow|\bshadow-(?!none\b)[a-z0-9\[]+|\bshadow\b(?=[\s\"'])", "shadow or glow"),
    ("blur", r"backdrop-filter|filter\s*:\s*blur|\bbackdrop-blur|\bblur-(?:sm|md|lg|xl|2xl|3xl)\b", "blur / glassmorphism"),
    ("border", r"\bborder(?:-(?:top|bottom|left|right|block|inline)(?:-(?:start|end))?)?\s*:\s*(?!none|0(?:px)?\s*[;}\"']|0 none|transparent)[^;}\"']*\d[^;}\"']*(?:solid|dashed|dotted|double)", "visible border (use surface contrast)"),
    ("border", r"\bborder(?:-[trblxy])?(?:-\d)?\s(?=.*class)|\bdivide-[xy]\b|\bring-\d\b", "Tailwind border/divide/ring class"),
    ("caps", r"text-transform\s*:\s*uppercase|\buppercase\b(?=[^:]*[\"'])", "forced uppercase"),
    ("tracking", r"letter-spacing\s*:\s*(?!0|normal|-)[^;}\"']+|\btracking-(?:wide|wider|widest)\b", "wide letter-spacing"),
    ("motion", r"animation[^;{]*infinite|@keyframes\s+(?:pulse|ping|glow|blink|shimmer|float|bounce)|\banimate-(?:pulse|ping|bounce|spin)\b", "looping/attention animation (pulsing dots, glows, blinking)"),
    ("motion", r"transition\s*:\s*all|\btransition-all\b|:hover[^{]*\{[^}]*transform\s*:\s*(?:scale|translate)|hover:(?:scale|-?translate)-", "hover lift/scale or transition: all"),
    ("motion", r"cubic-bezier\([^)]*1\.[1-9]|IntersectionObserver|data-aos|\breveal\b", "springy easing or scroll-reveal"),
    ("font", r"font-family\s*:[^;]*\b(?:Inter|Space Grotesk|Geist|Manrope|Plus Jakarta|Instrument Serif|Fraunces|Poppins|Outfit)\b", "template display font"),
    ("dead-link", r"href=[\"']#[\"']", "href=\"#\" (control that goes nowhere)"),
    ("icon", r"lucide-sparkles|\bSparkles\b|✨", "sparkles icon / emoji"),
]

PHRASES = [
    r"\blive\b(?=\s*</)", r"all systems operational", r"\bnow in (?:beta|public beta|early access)\b", r"\bnow available\b",
    r"\bintroducing\b", r"\bis here\b", r"\bnew!?\s*</", r">\s*beta\s*<", r">\s*new\s*<", r">\s*popular\s*<", r">\s*pro\s*<",
    r"\bai[- ]powered\b", r"\bpowered by ai\b",
    r"trusted by", r"loved by", r"join (?:thousands|\d)", r"\d+[kKmM]\+", r"99\.9+%", r"no credit card required",
    r"get started\s*(?:—|-|–)?\s*(?:it'?s )?free", r"start for free", r"watch (?:the )?demo", r"book a (?:demo|call)",
    r"made with (?:❤|♥|love)", r"how it works", r"why choose", r"what (?:our )?(?:users|customers) say", r"ready to get started",
    r"\bsupercharge", r"\bseamless(?:ly)?\b", r"\beffortless(?:ly)?\b", r"\bblazing(?:ly)?\b", r"\bnext[- ]gen", r"\bunlock\b",
    r"\belevate\b", r"\bgame[- ]chang", r"\brevolutioni[sz]", r"\bcutting[- ]edge\b", r"\bsay goodbye to\b", r"\bunleash\b",
    r"\bbuilt for (?:the )?(?:modern|developers|teams)\b", r"\bwelcome back\b", r"\boops!?\b", r"\bclick here\b", r"\blearn more\b",
    r">\s*submit\s*<", r"\bnot just\b", r"\bmore than just\b",
]

EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐⭕✅❌]")
HEX = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
CSS_COMMENT = re.compile(r"/\*.*?\*/", re.S)


def visible_lines(text):
    return CSS_COMMENT.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text).splitlines()


def scan(path):
    hits = []
    lines = visible_lines(path.read_text(errors="replace"))
    for n, line in enumerate(lines, 1):
        low = line.lower()
        for rule, rx, msg in RULES:
            m = re.search(rx, line, re.I)
            if m:
                hits.append((n, rule, msg, m.group(0)))
        for rx in PHRASES:
            m = re.search(rx, low)
            if m:
                hits.append((n, "copy", "slop phrase", m.group(0)))
        m = EMOJI.search(line)
        if m:
            hits.append((n, "emoji", "emoji in UI", m.group(0)))
        for m in HEX.finditer(line):
            h = m.group(1).lower()
            if len(h) == 3:
                h = "".join(c * 2 for c in h)
            if h not in CATPPUCCIN and not re.search(r"&#|url\(|href=|\bid=", line[max(0, m.start() - 8):m.start()]):
                hits.append((n, "palette", "colour outside Catppuccin Mocha/Latte", m.group(0)))
    return hits


def main(args):
    if not args:
        print(__doc__)
        return 2
    files = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            files += [f for f in sorted(p.rglob("*")) if f.suffix in EXTS and "node_modules" not in f.parts]
        elif p.exists():
            files.append(p)
    total = 0
    for f in files:
        for n, rule, msg, snip in scan(f):
            total += 1
            print(f"{f}:{n}  [{rule}] {msg}: {snip.strip()[:70]}")
    print(f"\n{total} hit(s) in {len(files)} file(s)." if total else f"clean: {len(files)} file(s), no hits.")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
