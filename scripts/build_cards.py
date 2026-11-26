#!/usr/bin/env python3
"""Build the retro SVG cards used by README.md (standard library only).

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

# Colour themes. "fieldnotes" matches https://aditya00801.github.io/
THEMES = {
    "fieldnotes": dict(paper="#E8E9DF", deep="#DFE2D5", ink="#2E3D28", soft="#46523F", accent="#536448",
                       second="#A9B887", hi="#2E3D28", rule="#B7BEA9", tiers=("#A9B887", "#718064", "#2E3D28")),
    "sunset": dict(paper="#F6EFD9", deep="#EDE0BF", ink="#3B2A20", soft="#5A4436", accent="#1F6F78",
                   second="#E3A72F", hi="#D1602C", rule="#D3BF92", tiers=("#1F6F78", "#E3A72F", "#D1602C")),
    "blend": dict(paper="#E8E9DF", deep="#DFE2D5", ink="#2E3D28", soft="#46523F", accent="#536448",
                  second="#E3A72F", hi="#D1602C", rule="#B7BEA9", tiers=("#536448", "#E3A72F", "#D1602C")),
}
THEME = os.environ.get("THEME", "fieldnotes")
C = THEMES[THEME]
PAPER, DEEP, INK, SOFT, ACCENT, SECOND, HI, RULE = (
    C[k] for k in ("paper", "deep", "ink", "soft", "accent", "second", "hi", "rule"))
SANS = "Arial,Helvetica,sans-serif"
MONO = "'Courier New',Courier,monospace"
SERIF = "Georgia,'Times New Roman',serif"

# ---------------------------------------------------------------- CONTENT
LEAD = ["I’m a final-year Computer Science & Engineering student specializing in",
        "Artificial Intelligence at Babu Banarasi Das University, Lucknow."]
ABOUT = ["I like taking ideas from notebooks to working software, whether that means preparing",
         "a dataset, testing a model, or making a tool someone can actually use. I’m looking for",
         "an internship or an early-career team where I can learn by building."]
TOOLKIT = [
    ("Code", ["Python · C++ · C · SQL"]),
    ("Machine learning", ["Scikit-learn · TensorFlow · CatBoost", "Optuna · feature engineering"]),
    ("Agentic AI", ["LLMs · AI agents · multi-agent systems", "Pydantic · automation"]),
    ("Data", ["Pandas · NumPy · EDA", "visualization · statistical analysis"]),
    ("Backend & security", ["REST APIs · FastAPI · HTTP", "threat detection · security logging"]),
    ("Development", ["Git · GitHub · Linux · WSL", "Jupyter · Streamlit"]),
]
PROJECTS = [
    ("student-stress", "Student Lifestyle & Stress Prediction", "DEPLOYED",
     "End-to-end app predicting health conditions in three categories. CatBoost on 690,088 records with 20 engineered features: 94.985% balanced accuracy.",
     "CatBoost · Optuna · Streamlit"),
    ("cyber-shield", "CyberShield-Auto", "IN DEVELOPMENT",
     "AI-driven cybersecurity platform combining machine learning, multi-agent workflows and security event analysis to spot and rate suspicious activity.",
     "AI Agents · FastAPI · Pydantic"),
    ("brain-tumor", "Brain Tumor Detection", "DEEP LEARNING",
     "CNN that classifies brain MRI scans as glioma, meningioma, pituitary or no tumor, served with Streamlit.",
     "TensorFlow · Keras · Streamlit"),
    ("coral-reef", "Coral Reef Health Monitoring", "TEAM PROJECT",
     "Transfer-learning CNN that tells bleached from healthy coral, with a Streamlit app. 92% reported accuracy.",
     "TensorFlow · OpenCV · Streamlit"),
]
LOGBOOK = [
    ("27 AUG 2026", "Oracle Agentic AI Certified Foundations Associate", "Oracle University"),
    ("26 AUG 2026", "MongoDB Overview: Core Concepts and Architecture", "MongoDB"),
    ("14 APR 2026", "Deloitte Data Analytics Job Simulation", "Forage"),
    ("09–11 MAR 2026", "SQL Bootcamp", "LetsUpgrade"),
    ("09–10 FEB 2026", "Git & GitHub Bootcamp", "LetsUpgrade"),
    ("28 NOV 2025", "JPMorgan Chase Software Engineering Job Simulation", "Forage · Kafka, H2, REST APIs"),
    ("17 OCT 2025", "Oracle Cloud Infrastructure 2025 Certified Data Science Professional", "Oracle · valid through October 2027"),
    ("13 SEP 2025", "Intro to Machine Learning", "Kaggle"),
    ("MAY 2025", "HackHazards ’25 participant", "Team Hack Heroes · The NAMESPACE Community"),
]


# ---------------------------------------------------------------- HELPERS
def text(x, y, value, size=14, fill=INK, weight=400, font=SANS, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}" text-anchor="{anchor}" {extra}>{escape(str(value))}</text>')


def shade(colour, factor):
    return "#" + "".join(f"{int(int(colour[i:i+2], 16) * factor):02x}" for i in (1, 3, 5))


def box(x, y, w, h, fill=PAPER, stroke=INK):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}"/>'


def eyebrow(x, y, value):
    return text(x, y, value, 12, ACCENT, 700, MONO, extra='letter-spacing="1.2"')


def card(name, width, height, body, label, kicker=None, title=None, style=""):
    head = ""
    if kicker:
        head = eyebrow(28, 36, kicker) + text(28, 68, title, 27, INK, 500, extra='letter-spacing="-0.8"')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
           f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(label, {chr(34): "&quot;"})}">'
           f'<defs><pattern id="dots" width="7" height="7" patternUnits="userSpaceOnUse">'
           f'<circle cx="1" cy="1" r=".6" fill="{INK}" opacity=".13"/></pattern></defs>'
           f'<style>{style}@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>'
           f'<rect x="7" y="7" width="{width-8}" height="{height-8}" fill="{INK}"/>'
           f'{box(1, 1, width-8, height-8)}'
           f'<rect x="1" y="1" width="{width-8}" height="{height-8}" fill="url(#dots)"/>'
           f'{head}{body}</svg>\n')
    (ASSETS / f"{name}.svg").write_text(svg, encoding="utf-8")


# ---------------------------------------------------------------- CARDS
def hero():
    b = [f'<circle class="light" cx="32" cy="29" r="4" fill="{ACCENT}"/>',
         text(44, 33, "PERSONAL PROFILE / 2026", 11, ACCENT, 400, MONO),
         text(806, 33, "LUCKNOW, INDIA ✳", 11, ACCENT, 400, MONO, "end"),
         f'<line x1="28" y1="48" x2="806" y2="48" stroke="{RULE}"/>',
         eyebrow(28, 84, "ADITYA KUSHWAHA — COMPUTER SCIENCE / AI"),
         text(28, 138, "Building useful things with", 42, INK, 500, extra='letter-spacing="-1.8"'),
         text(28, 188, "intelligent software.", 44, HI, 400, SERIF, extra='font-style="italic" letter-spacing="-1.8"'),
         text(28, 224, "Machine learning, agentic AI, and the software that brings them into the real world.", 14, SOFT),
         f'<rect x="28" y="250" width="8" height="8" fill="{HI}"/>',
         text(44, 258, "OPEN TO INTERNSHIPS & EARLY-CAREER ROLES", 12, ACCENT, 700, MONO),
         f'<ellipse class="orbit" cx="704" cy="134" rx="104" ry="52" fill="none" stroke="{ACCENT}" stroke-dasharray="5 6"/>',
         f'<g class="float"><rect x="672" y="102" width="82" height="82" fill="{INK}"/>'
         f'{box(664, 94, 82, 82, SECOND)}'
         + text(705, 139, "AK.", 28, INK, 900, MONO, "middle")
         + text(705, 160, "AI / SWE", 10, INK, 700, MONO, "middle") + "</g>"]
    style = ("@keyframes f{50%{transform:translateY(-7px)}}.float{animation:f 7s ease-in-out infinite}"
             "@keyframes o{to{stroke-dashoffset:-220}}.orbit{animation:o 18s linear infinite}"
             "@keyframes l{50%{opacity:.3}}.light{animation:l 2.4s ease-in-out infinite}")
    card("hero", 840, 288, "".join(b),
         "Aditya Kushwaha: building useful things with intelligent software. Open to internships and early-career roles.",
         style=style)


def about():
    b = [text(28, 110 + i * 25, line, 17, INK) for i, line in enumerate(LEAD)]
    b += [text(28, 174 + i * 22, line, 14, SOFT) for i, line in enumerate(ABOUT)]
    card("about", 840, 250, "".join(b), " ".join(LEAD + ABOUT), "01 / A SHORT INTRODUCTION",
         "Curiosity, with something to show for it.")


def toolkit():
    b = []
    for i, (name, lines) in enumerate(TOOLKIT):
        x, y = 28 + (i % 2) * 389, 92 + (i // 2) * 92
        b.append(box(x, y, 389, 92, "none", RULE) + text(x + 16, y + 28, "ABCDEF"[i], 12, ACCENT, 400, MONO)
                 + text(x + 44, y + 28, name, 15, INK, 700, MONO))
        b += [text(x + 44, y + 52 + n * 20, line, 13, SOFT) for n, line in enumerate(lines)]
    label = "Toolkit: " + "; ".join(f"{n}: {' '.join(l)}" for n, l in TOOLKIT)
    card("stack", 840, 396, "".join(b), label, "02 / TOOLS I REACH FOR", "The toolkit")


def projects():
    for number, (slug, title, status, desc, tech) in enumerate(PROJECTS, 1):
        b = [text(20, 30, f"PROJECT / 0{number}", 11, ACCENT, 400, MONO),
             text(382, 30, status, 11, ACCENT, 700, MONO, "end"),
             text(20, 68, title, 17.5, INK, 700, extra='letter-spacing="-0.5"')]
        b += [text(20, 96 + i * 20, line, 13, SOFT) for i, line in enumerate(textwrap.wrap(desc, 55)[:4])]
        b.append(f'<line x1="20" y1="174" x2="382" y2="174" stroke="{RULE}"/>')
        b.append(text(20, 196, tech, 12, ACCENT, 700, MONO))
        card(f"project-{slug}", 410, 220, "".join(b), f"{title}: {desc}")


def logbook():
    b = []
    for i, (date, name, issuer) in enumerate(LOGBOOK):
        y = 92 + i * 48
        b.append(f'<line x1="28" y1="{y}" x2="806" y2="{y}" stroke="{RULE}"/>'
                 + text(28, y + 22, date, 11, ACCENT, 400, MONO)
                 + text(158, y + 22, name, 14, INK, 700)
                 + text(158, y + 39, issuer, 12, SOFT)
                 + text(806, y + 22, f"{len(LOGBOOK) - i:02d}", 11, ACCENT, 400, MONO, "end"))
    label = "Logbook: " + "; ".join(f"{n} ({d})" for d, n, _ in LOGBOOK)
    card("logbook", 840, 92 + len(LOGBOOK) * 48 + 22, "".join(b), label, "04 / RECENT MILESTONES", "The logbook")


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
        x = 28 + i * 157
        b.append(box(x, 90, 148, 90, DEEP)
                 + text(x + 74, 136, f"{value:,}", 32, HI, 400, SERIF, "middle")
                 + text(x + 74, 163, name, 10.5, SOFT, 400, MONO, "middle"))
    label = "GitHub activity, last 12 months: " + ", ".join(f"{v} {n}" for v, n in items)
    card("stats", 840, 208, "".join(b), label, "GITHUB / LAST 12 MONTHS", "Activity")


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
        b.append(poly([pt(w, d), pt(w + .86, d), pt(w + .86, d + .86), pt(w, d + .86)], DEEP if THEME == "sunset" else RULE))
    for w, d, count in sorted(cells, key=lambda c: c[0] * uy + c[1] * vy):
        if not count:
            continue
        level = (count / peak) ** 0.5
        h = 10 + 92 * level
        top = C["tiers"][0 if level < .35 else 1 if level < .65 else 2]
        left, right = shade(top, .82), shade(top, .66)
        a, e = .08, .78
        # buildings rise one week after another, from left to right
        b.append(f'<g class="rise" style="animation-delay:{w * .045:.2f}s">')
        b.append(poly([pt(w + a, d + e), pt(w + e, d + e), pt(w + e, d + e, h), pt(w + a, d + e, h)], left))
        b.append(poly([pt(w + e, d + a), pt(w + e, d + e), pt(w + e, d + e, h), pt(w + e, d + a, h)], right))
        b.append(poly([pt(w + a, d + a, h), pt(w + e, d + a, h), pt(w + e, d + e, h), pt(w + a, d + e, h)], top))
        # lit windows
        for k, z in enumerate(range(8, int(h) - 5, 10)):
            b.append(poly([pt(w + .27, d + e, z), pt(w + .52, d + e, z), pt(w + .52, d + e, z + 4),
                           pt(w + .27, d + e, z + 4)], PAPER, f'class="w{(w + d + k) % 3}"'))
        b.append("</g>")
        if (w, d) == newest:
            x, y = pt(w + .43, d + .43, h + 9).split(",")
            beacon = (f'<g class="beacon"><circle class="ring" cx="{x}" cy="{y}" r="4" fill="none" stroke="{HI}" '
                      f'stroke-width="1.5"/><circle cx="{x}" cy="{y}" r="2.5" fill="{HI}"/></g>')
    b.append(beacon)  # marks the most recent active day
    total = sum(d["count"] for d in days)
    b.append(text(806, 36, f"{total:,} CONTRIBUTIONS", 12, ACCENT, 700, MONO, "end"))
    b.append(text(806, 458, f"taller = busier · beacon = latest active day · updated {updated}", 11, ACCENT, 400, MONO, "end"))
    style = ("@keyframes t{0%,100%{opacity:.95}50%{opacity:.25}}"
             ".w0{animation:t 4s infinite}.w1{animation:t 5s 1.3s infinite}.w2{animation:t 6s 2.1s infinite}"
             "@keyframes rise{from{transform:scaleY(0);opacity:0}to{transform:scaleY(1);opacity:1}}"
             ".rise{transform-box:fill-box;transform-origin:50% 100%;animation:rise 1s cubic-bezier(.2,.8,.2,1) backwards}"
             "@keyframes show{from{opacity:0}}.beacon{animation:show .6s 3.2s backwards}"
             "@keyframes ping{0%{transform:scale(.6);opacity:1}100%{transform:scale(3);opacity:0}}"
             ".ring{transform-box:fill-box;transform-origin:center;animation:ping 1.8s ease-out infinite}"
             )
    card("city", 840, 480, "".join(b),
         f"Contribution city: {total} contributions in the last 12 months", "GITHUB / DAY BY DAY",
         "Contribution city", style)


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


def export_profile():
    """Share the text with the interactive page in docs/, so it is edited in one place."""
    profile = {"lead": " ".join(LEAD), "about": " ".join(ABOUT),
               "toolkit": [{"name": n, "detail": " · ".join(l)} for n, l in TOOLKIT],
               "projects": [{"slug": s, "title": t, "status": st, "description": d, "tech": tech}
                            for s, t, st, d, tech in PROJECTS],
               "logbook": [{"date": d, "title": t, "issuer": i} for d, t, i in LOGBOOK]}
    (ROOT / "data" / "profile.json").write_text(
        json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    ASSETS.mkdir(exist_ok=True)
    if "--fetch" in sys.argv:
        fetch()
    data = json.loads(DATA.read_text())
    hero()
    about()
    toolkit()
    projects()
    logbook()
    export_profile()
    stats(data["days"])
    city(data["days"], data["updated"])


if __name__ == "__main__":
    main()
