#!/usr/bin/env python3
"""Build the teal SVG cards used by README.md (standard library only).

  python3 scripts/build_cards.py           # rebuild from data/contributions.json
  python3 scripts/build_cards.py --fetch   # refresh the data first (needs GITHUB_TOKEN)

Edit the text in the CONTENT section, then run the script again.
"""
import datetime as dt
import json
import os
import sys
import textwrap
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

USER = "aditya00801"
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
DATA = ROOT / "data" / "contributions.json"

BG0, BG1, EDGE = "#061a1f", "#0b2a30", "#145c5a"
TEAL, MINT, TEXT, MUTED = "#2dd4bf", "#99f6e4", "#e6fffb", "#8fbdb8"
SANS = "'Segoe UI',Ubuntu,Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','Fira Code',Consolas,Menlo,monospace"

# ---------------------------------------------------------------- CONTENT
ABOUT = [
    "I build practical AI solutions with machine learning, deep learning and",
    "computer vision, and explore where AI meets cybersecurity.",
]
FOCUS = ["Deep Learning & Computer Vision", "MLOps & Generative AI",
         "Ethical hacking & intrusion detection", "DSA, System Design & Backend"]
FACTS = [("Degree", "B.Tech CSE (Artificial Intelligence)"),
         ("University", "Babu Banarasi Das University"),
         ("Location", "Lucknow, India"),
         ("Language", "Python")]
STACK = [
    ("Languages", ["Python", "C", "C++", "MySQL"]),
    ("AI / ML", ["TensorFlow", "Keras", "PyTorch", "Scikit-Learn", "OpenCV"]),
    ("Data Science", ["NumPy", "Pandas", "Matplotlib", "Seaborn", "Jupyter"]),
    ("Frameworks", ["Flask", "Streamlit"]),
    ("Security", ["Kali Linux", "Wireshark", "Nmap", "Metasploit"]),
    ("Tools", ["Git", "GitHub", "VS Code", "Google Colab", "Linux", "Antigravity"]),
]
PROJECTS = [
    ("cyber-shield", "CyberShield-Auto", "In development",
     "AI-powered cyber threat detection. Preparing the CICIDS2017 dataset for a multiclass intrusion detection model.",
     "Python · CICIDS2017 · Jupyter"),
    ("brain-tumor", "Brain Tumor Detection", "Deep learning",
     "CNN that classifies brain MRI scans as glioma, meningioma, pituitary or no tumor, served with Streamlit.",
     "TensorFlow · Keras · Streamlit"),
    ("coral-reef", "Coral Reef Health Monitoring", "Team project",
     "Transfer-learning CNN that tells bleached from healthy coral, with a Streamlit app. 92% reported accuracy.",
     "TensorFlow · OpenCV · Streamlit"),
    ("student-stress", "Student Lifestyle & Stress", "Kaggle S6E7",
     "End-to-end ML for a Playground Series competition: feature engineering and balanced accuracy tuning.",
     "Random Forest · CatBoost"),
]
CERTS = [
    ("Agentic AI Certified Foundations Associate", "Oracle", "Aug 2026"),
    ("MongoDB Overview: Core Concepts and Architecture", "MongoDB", "Aug 2026"),
    ("Data Analytics Job Simulation", "Deloitte · Forage", "Apr 2026"),
    ("SQL Bootcamp", "LetsUpgrade", "Mar 2026"),
    ("Git & GitHub Bootcamp", "LetsUpgrade", "Feb 2026"),
    ("Software Engineering Job Simulation", "JPMorgan Chase · Forage", "Nov 2025"),
    ("OCI 2025 Certified Data Science Professional", "Oracle", "Oct 2025"),
    ("Intro to Machine Learning", "Kaggle", "Sep 2025"),
]


# ---------------------------------------------------------------- HELPERS
def text(x, y, value, size=14, fill=TEXT, weight=400, font=SANS, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}" text-anchor="{anchor}" {extra}>{escape(str(value))}</text>')


def card(name, width, height, body, label, title=None, style=""):
    head = ""
    if title:
        head = (f'<rect x="28" y="24" width="4" height="20" rx="2" fill="{TEAL}"/>'
                + text(42, 41, title, 19, TEXT, 700))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
           f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(label, {chr(34): "&quot;"})}">'
           f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
           f'<stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/></linearGradient></defs>'
           f'<style>{style}</style>'
           f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="16" fill="url(#bg)" stroke="{EDGE}" stroke-width="1.5"/>'
           f'{head}{body}</svg>\n')
    (ASSETS / f"{name}.svg").write_text(svg, encoding="utf-8")


# ---------------------------------------------------------------- CARDS
def hero():
    b = [f'<circle cx="760" cy="40" r="120" fill="{TEAL}" opacity="0.07"/>',
         f'<circle cx="70" cy="220" r="100" fill="{TEAL}" opacity="0.06"/>',
         text(420, 62, "$ whoami", 15, TEAL, 400, MONO, "middle"),
         text(420, 120, "Aditya Kushwaha", 52, TEXT, 800, SANS, "middle"),
         text(420, 158, "AI / ML  ·  Cybersecurity  ·  Data Science", 20, MINT, 600, SANS, "middle"),
         text(420, 196, "Code • Learn • Build • Contribute • Repeat", 15, MUTED, 400, MONO, "middle"),
         f'<rect class="line" x="360" y="212" width="120" height="3" rx="1.5" fill="{TEAL}"/>']
    style = ("@keyframes p{0%,100%{opacity:.35}50%{opacity:1}}.line{animation:p 3s ease-in-out infinite}")
    card("hero", 840, 240, "".join(b), "Aditya Kushwaha: AI/ML, Cybersecurity, Data Science", style=style)


def about():
    b = [text(28, 76 + i * 22, line, 15, MUTED) for i, line in enumerate(ABOUT)]
    b.append(text(28, 142, "CURRENT FOCUS", 12, TEAL, 700))
    for i, item in enumerate(FOCUS):
        y = 170 + i * 27
        b.append(f'<circle cx="34" cy="{y-5}" r="3.5" fill="{TEAL}"/>' + text(48, y, item, 15))
    b.append(f'<rect x="458" y="130" width="354" height="148" rx="12" fill="#04151a" stroke="{EDGE}"/>')
    for i, (key, value) in enumerate(FACTS):
        y = 158 + i * 31
        b.append(text(476, y, key, 12, TEAL, 400, MONO) + text(576, y, value, 13, TEXT))
    card("about", 840, 304, "".join(b), "About: " + " ".join(ABOUT), "About Me")


def stack():
    b, y = [], 66
    for group, items in STACK:
        b.append(text(28, y + 19, group, 13, TEAL, 700))
        x = 170
        for item in items:
            w = int(len(item) * 7.8) + 26
            b.append(f'<rect x="{x}" y="{y}" width="{w}" height="28" rx="14" fill="#0e3a3c" stroke="{EDGE}"/>'
                     + text(x + w / 2, y + 19, item, 13, TEXT, 500, SANS, "middle"))
            x += w + 10
        y += 42
    label = "Tech stack: " + "; ".join(f"{g}: {', '.join(i)}" for g, i in STACK)
    card("stack", 840, y + 14, "".join(b), label, "Tech Stack")


def projects():
    for slug, title, tag, desc, tech in PROJECTS:
        tw = int(len(tag) * 6.8) + 22
        b = [f'<rect x="22" y="20" width="{tw}" height="22" rx="11" fill="#0e3a3c" stroke="{TEAL}"/>',
             text(22 + tw / 2, 35, tag, 11, MINT, 600, SANS, "middle"),
             text(22, 72, title, 19, TEXT, 700)]
        b += [text(22, 100 + i * 20, line, 13, MUTED) for i, line in enumerate(textwrap.wrap(desc, 56)[:4])]
        b.append(text(22, 188, tech, 12, TEAL, 400, MONO))
        card(f"project-{slug}", 410, 208, "".join(b), f"{title}: {desc}")


def certifications():
    b = []
    for i, (name, issuer, date) in enumerate(CERTS):
        y = 78 + i * 34
        b.append(f'<path d="M34 {y-11}l6 6-6 6-6-6z" fill="{TEAL}"/>'
                 + text(52, y, name, 14, TEXT, 600)
                 + text(620, y, issuer, 12, MUTED, 400, SANS, "end")
                 + text(812, y, date, 12, TEAL, 400, MONO, "end"))
    label = "Certifications: " + "; ".join(f"{n} ({i}, {d})" for n, i, d in CERTS)
    card("certifications", 840, 78 + len(CERTS) * 34, "".join(b), label, "Certificates & Courses")


def stats(days):
    counts = [d["count"] for d in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    # A day that is still empty today does not break the current streak.
    tail = counts[:-1] if counts and counts[-1] == 0 else counts
    current = 0
    for c in reversed(tail):
        if not c:
            break
        current += 1
    items = [(sum(counts), "contributions"), (sum(1 for c in counts if c), "active days"),
             (current, "current streak (days)"), (longest, "longest streak (days)"),
             (max(counts, default=0), "best day")]
    b = []
    for i, (value, name) in enumerate(items):
        x = 28 + i * 159
        b.append(f'<rect x="{x}" y="64" width="148" height="86" rx="12" fill="#04151a" stroke="{EDGE}"/>'
                 + text(x + 74, 108, f"{value:,}", 30, TEAL, 800, SANS, "middle")
                 + text(x + 74, 133, name, 11, MUTED, 400, SANS, "middle"))
    label = "GitHub activity, last 12 months: " + ", ".join(f"{v} {n}" for v, n in items)
    card("stats", 840, 174, "".join(b), label, "GitHub Activity · last 12 months")


def city(days, updated):
    first = dt.date.fromisoformat(days[0]["date"])
    start = first - dt.timedelta(days=(first.weekday() + 1) % 7)  # Sunday
    peak = max((d["count"] for d in days), default=0) or 1
    cells = []
    for d in days:
        offset = (dt.date.fromisoformat(d["date"]) - start).days
        cells.append((offset // 7, offset % 7, d["count"]))
    # isometric grid: weeks run to the lower right, weekdays to the lower left
    ux, uy, vx, vy = 12.8, 3.7, -9.6, 7.0
    ox, oy = 108, 150

    def pt(w, d, h=0):
        return f"{ox + w*ux + d*vx:.1f},{oy + w*uy + d*vy - h:.1f}"

    def poly(points, fill, extra=""):
        return f'<polygon points="{" ".join(points)}" fill="{fill}" {extra}/>'

    b = []
    newest = next(((w, d) for w, d, count in reversed(cells) if count), None)
    beacon = ""
    # Draw the ground first so no tile covers a building while it rises.
    for w, d, count in cells:
        b.append(poly([pt(w, d), pt(w + .86, d), pt(w + .86, d + .86), pt(w, d + .86)], "#10393d"))
    for w, d, count in sorted(cells, key=lambda c: c[0] * uy + c[1] * vy):
        if not count:
            continue
        level = (count / peak) ** 0.5
        h = 10 + 92 * level
        top, left, right = (("#5eead4", "#0f766e", "#115e59") if level < .35 else
                            ("#7ff0dc", "#0d9488", "#0f766e") if level < .65 else
                            ("#ccfbf1", "#14b8a6", "#0d9488"))
        a, e = .08, .78
        # buildings rise one week after another, from left to right
        b.append(f'<g class="rise" style="animation-delay:{w * .045:.2f}s">')
        b.append(poly([pt(w + a, d + e), pt(w + e, d + e), pt(w + e, d + e, h), pt(w + a, d + e, h)], left))
        b.append(poly([pt(w + e, d + a), pt(w + e, d + e), pt(w + e, d + e, h), pt(w + e, d + a, h)], right))
        b.append(poly([pt(w + a, d + a, h), pt(w + e, d + a, h), pt(w + e, d + e, h), pt(w + a, d + e, h)], top))
        # lit windows
        for k, z in enumerate(range(8, int(h) - 5, 10)):
            b.append(poly([pt(w + .27, d + e, z), pt(w + .52, d + e, z), pt(w + .52, d + e, z + 4),
                           pt(w + .27, d + e, z + 4)], "#fef9c3", f'class="w{(w + d + k) % 3}"'))
        b.append("</g>")
        if (w, d) == newest:
            x, y = pt(w + .43, d + .43, h + 9).split(",")
            beacon = (f'<g class="beacon"><circle class="ring" cx="{x}" cy="{y}" r="4" fill="none" stroke="#fde68a" '
                      f'stroke-width="1.5"/><circle cx="{x}" cy="{y}" r="2.5" fill="#fde68a"/></g>')
    b.append(beacon)  # marks the most recent active day
    for i, (x, y) in enumerate([(300, 70), (420, 96), (520, 58), (640, 84), (730, 130), (780, 60),
                                (230, 104), (80, 330), (200, 372), (330, 394)]):
        b.append(f'<circle class="w{i % 3}" cx="{x}" cy="{y}" r="1.4" fill="{MINT}"/>')
    total = sum(d["count"] for d in days)
    b.append(text(812, 40, f"{total:,} contributions", 14, MINT, 600, SANS, "end"))
    b.append(text(812, 462, f"taller = busier · beacon = latest active day · updated {updated}", 11, MUTED, 400, MONO, "end"))
    style = ("@keyframes t{0%,100%{opacity:.95}50%{opacity:.25}}"
             ".w0{animation:t 4s infinite}.w1{animation:t 5s 1.3s infinite}.w2{animation:t 6s 2.1s infinite}"
             "@keyframes rise{from{transform:scaleY(0);opacity:0}to{transform:scaleY(1);opacity:1}}"
             ".rise{transform-box:fill-box;transform-origin:50% 100%;animation:rise 1s cubic-bezier(.2,.8,.2,1) backwards}"
             "@keyframes show{from{opacity:0}}.beacon{animation:show .6s 3.2s backwards}"
             "@keyframes ping{0%{transform:scale(.6);opacity:1}100%{transform:scale(3);opacity:0}}"
             ".ring{transform-box:fill-box;transform-origin:center;animation:ping 1.8s ease-out infinite}"
             "@media (prefers-reduced-motion:reduce){*{animation:none!important}}")
    card("city", 840, 480, "".join(b),
         f"Contribution city: {total} contributions in the last 12 months", "Contribution City", style)


# ---------------------------------------------------------------- DATA
def fetch():
    token = os.environ["GITHUB_TOKEN"]
    query = ("query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{"
             "weeks{contributionDays{date contributionCount}}}}}}")
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": {"u": USER}}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": USER})
    with urllib.request.urlopen(req, timeout=30) as res:
        payload = json.load(res)
    if payload.get("errors"):
        sys.exit(f"GitHub API error: {payload['errors']}")
    weeks = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    days = [{"date": d["date"], "count": d["contributionCount"]} for w in weeks for d in w["contributionDays"]]
    DATA.write_text(json.dumps({"updated": dt.date.today().isoformat(), "days": days}) + "\n")


def main():
    ASSETS.mkdir(exist_ok=True)
    if "--fetch" in sys.argv:
        fetch()
    data = json.loads(DATA.read_text())
    hero()
    about()
    stack()
    projects()
    certifications()
    stats(data["days"])
    city(data["days"], data["updated"])


if __name__ == "__main__":
    main()
