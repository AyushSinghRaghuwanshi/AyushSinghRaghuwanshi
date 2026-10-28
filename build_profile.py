#!/usr/bin/env python3
"""Build the animated SVGs for github.com/AyushSinghRaghuwanshi.

    python scripts/build_profile.py

The profile speaks GitHub's own language: a career drawn as a `git log --graph`,
a pull request whose CI checks are real, measured results, and skills as topic
pills. Soft pastel GitHub colours, readable on both light and dark mode.
Pure SVG + CSS (no JavaScript, no web fonts), so GitHub animates it inside <img>.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

# GitHub's own palette, softened to pastels
C = dict(
    paper="#fdfcfa", line="#e6e3ee", fg="#2f3542", muted="#7a8091", faint="#f6f5f9",
    green="#4fb871", green_t="#e3f7e8", green_d="#2c8a4c",
    blue="#5b9be6", blue_t="#e3f0fd", blue_d="#2f6fbd",
    purple="#9a7fe0", purple_t="#efe9fd", purple_d="#6b4fc4",
    amber="#e3ac3f", amber_t="#fdf3dc", amber_d="#a77610",
    pink="#e88aa8", pink_t="#fce8ef", pink_d="#b9506f",
    main="#b9b4c9",
)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w, h, body, style, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{esc(label)}" fill="none">\n<style>\ntext{{font-family:{SANS}}} .m{{font-family:{MONO}}}\n'
            f'.fi{{opacity:0;animation:fi .6s ease-out forwards}} @keyframes fi{{to{{opacity:1}}}}\n'
            f'@media (prefers-reduced-motion: reduce){{*{{animation:none!important;opacity:1!important;stroke-dashoffset:0!important}}}}\n'
            f'{style}</style>\n<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="12" fill="{C["paper"]}" stroke="{C["line"]}"/>\n'
            f'{body}\n</svg>\n')


def pill(x, y, text, fg, bg, size=11.5, cls="", delay=None, mono=True, pad=9, h=21):
    w = len(text) * size * (0.61 if mono else 0.56) + pad * 2
    st = f' style="animation-delay:{delay:.2f}s"' if delay is not None else ""
    return (f'<g class="{cls}"{st}><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="{bg}" stroke="{fg}" stroke-opacity=".35"/>'
            f'<text class="{"m" if mono else ""}" x="{x + pad:.1f}" y="{y + h / 2 + size * .36:.1f}" font-size="{size}" fill="{fg}">{esc(text)}</text></g>'), w


# ------------------------------------------------------------------ header: career as git log --graph
def header():
    W = 1000
    LX = [56, 82, 108]                       # lane x positions: main, lane 1, lane 2
    TOP, RH = 132, 31
    # rows, newest first: (lane, branch colour, message, refs, date)
    rows = [
        (0, "green", "Open to AI / ML engineer roles across the UK", ["HEAD → main", "open-to-work"], "now"),
        (2, "pink", "DocFlow: QLoRA fine-tuned VLM lifts field accuracy 85.5% → 91.3%", ["feat/docflow"], "2026"),
        (0, "purple", "Merge msc/applied-ai: MSc Applied AI, University of Warwick", [], "Sep 2026"),
        (1, "purple", "LineGuard: 3rd place, AAI Tech Talks Hackathon (secure RAG)", [], "Jun 2026"),
        (1, "purple", "AWS Certified Machine Learning Engineer – Associate", [], "Mar 2026"),
        (1, "purple", "Start MSc Applied AI at Warwick", ["msc/applied-ai"], "Sep 2025"),
        (0, "blue", "Merge job/cybage: 3 yrs production, −40% recurring issues, +35% deployment reliability", [], "Jun 2025"),
        (1, "blue", "Ship ~7 features a month; releases through Azure DevOps CI/CD", [], "2022–25"),
        (1, "blue", "Join Cybage as Software Engineer: own a central .NET Core REST API", ["job/cybage"], "Aug 2022"),
        (0, "green", "Merge b.e.-it: B.E. Information Technology, CGPA 9.04 / 10", [], "2022"),
        (1, "green", "Publish 2 papers at IEEE GECOST", [], "2022"),
        (1, "green", "Publish in IRJET: graph CNNs for outlier detection", [], "2021"),
        (1, "amber", "Data Science Intern at TechnoColabs", [], "2021"),
        (0, "green", "Initial commit: start B.E. Information Technology", ["b.e.-it"], "2018"),
    ]
    # branches: lane, colour, first row, last row (line extent), row merged into on main, row forked from on main
    branches = [
        (2, "pink", 1, 5, None, 6),
        (1, "purple", 3, 5, 2, 6),
        (1, "blue", 7, 8, 6, 9),
        (1, "green", 10, 12, 9, 13),
    ]

    def Y(i):
        return TOP + i * RH

    segs = {i: [] for i in range(len(rows))}
    for i in range(len(rows) - 1):
        segs[i].append((f"M{LX[0]} {Y(i)} V{Y(i + 1)}", C["main"]))
    for lane, col, a, b, merge, fork in branches:
        x = LX[lane]
        for i in range(a, b):
            segs[i].append((f"M{x} {Y(i)} V{Y(i + 1)}", C[col]))
        if merge is not None:
            segs[merge].append((f"M{LX[0]} {Y(merge)} C{LX[0]} {Y(merge) + RH * .6} {x} {Y(a) - RH * .6} {x} {Y(a)}", C[col]))
        segs[b].append((f"M{x} {Y(b)} C{x} {Y(b) + RH * .6} {LX[0]} {Y(fork) - RH * .6} {LX[0]} {Y(fork)}", C[col]))

    body = [
        f'<text x="40" y="56" font-size="30" font-weight="700" fill="{C["fg"]}">Ayush Singh Raghuwanshi</text>',
        f'<text x="40" y="84" font-size="15" fill="{C["muted"]}">AI Engineer · RAG, LLMs &amp; document AI · 3 yrs production engineering · Coventry, UK</text>',
        f'<text class="m" x="{W - 40}" y="54" font-size="12" fill="{C["muted"]}" text-anchor="end">$ git log --graph --oneline --all</text>',
        f'<line x1="32" y1="104" x2="{W - 32}" y2="104" stroke="{C["line"]}"/>',
    ]
    # draw edges first (under dots), each fading in with its row
    for i in range(len(rows)):
        d = .25 + i * .16
        body.append(f'<g class="row" style="animation-delay:{d:.2f}s">' +
                    "".join(f'<path d="{p}" stroke="{c}" stroke-width="2.6" stroke-linecap="round"/>' for p, c in segs[i]) + "</g>")
    for i, (lane, col, msg, refs, date) in enumerate(rows):
        d = .25 + i * .16
        y = Y(i)
        c, ct, cd = C[col], C[col + "_t"], C[col + "_d"]
        is_head = i == 0
        dot = (f'<circle class="pulse" cx="{LX[lane]}" cy="{y}" r="7" fill="{c}"/>' if is_head else
               f'<circle cx="{LX[lane]}" cy="{y}" r="5.6" fill="{C["paper"]}" stroke="{c}" stroke-width="2.6"/>')
        x = 140
        parts = [dot]
        for ref in refs:
            p, w = pill(x, y - 10.5, ref, cd, ct, size=11, h=21, pad=8)
            parts.append(p)
            x += w + 6
        if refs:
            x += 4
        parts.append(f'<text x="{x:.1f}" y="{y + 4.8}" font-size="13.5" fill="{C["fg"] if lane or is_head else C["fg"]}">{esc(msg)}</text>')
        parts.append(f'<text class="m" x="{W - 40}" y="{y + 4.5}" font-size="11.5" fill="{C["muted"]}" text-anchor="end">{esc(date)}</text>')
        body.append(f'<g class="row" style="animation-delay:{d:.2f}s">{"".join(parts)}</g>')
    H = Y(len(rows) - 1) + 34
    style = """
.row{opacity:0;animation:rw .45s ease-out forwards}
@keyframes rw{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}
.pulse{transform-box:fill-box;transform-origin:center;animation:pl 2.2s ease-in-out 2.6s infinite}
@keyframes pl{0%,100%{transform:scale(1)}50%{transform:scale(1.3)}}
"""
    return svg(W, H, "\n".join(body), style,
               "Ayush Singh Raghuwanshi, AI Engineer. Career as a git log: B.E. IT 2018–2022 with IEEE and IRJET papers, "
               "data science internship 2021, software engineer at Cybage 2022–2025, MSc Applied AI at Warwick 2025–2026 "
               "with AWS ML certification and a hackathon 3rd place, DocFlow at 91.3% field accuracy, now open to work.")


# ------------------------------------------------------------------ pull request with CI checks
def pull_request():
    W = 1000
    checks = [
        ("evals / docflow", "field accuracy 91.3%, up from 85.5% baseline · 347 SROIE receipts · McNemar significant"),
        ("evals / explainable-ai", "PR-AUC 0.80, up from 0.52 persistence baseline · held-out test · leakage-controlled"),
        ("evals / lineguard", "Hit@5 0.95, up from 0.80 · 3,785 CISA advisories · hybrid BM25 + BGE"),
        ("security / red-team", "4 / 4 prompt injections blocked · 0 fabricated citations in 120 outputs"),
        ("tests / docflow", "131 passed · GitHub Actions CI"),
        ("production / cybage", "3 yrs owning a .NET Core API · −40% recurring issues · +35% deployment reliability"),
        ("right-to-work / uk", "UK Graduate Route · no sponsorship needed"),
    ]
    body, style = [], []
    body.append(f'<text x="32" y="50" font-size="24" font-weight="600" fill="{C["fg"]}">Hire Ayush as your next AI Engineer <tspan fill="{C["muted"]}" font-weight="400">#2026</tspan></text>')
    body.append(f'<g><rect x="32" y="70" width="78" height="28" rx="14" fill="{C["green"]}"/>'
                f'<circle cx="51" cy="84" r="5" stroke="#fff" stroke-width="2"/><circle cx="51" cy="84" r="1.6" fill="#fff"/>'
                f'<text x="62" y="89" font-size="13" font-weight="600" fill="#fff">Open</text></g>')
    body.append(f'<text x="124" y="89" font-size="14" fill="{C["muted"]}"><tspan font-weight="600" fill="{C["fg"]}">AyushSinghRaghuwanshi</tspan> wants to merge '
                f'<tspan font-weight="600" fill="{C["fg"]}">3 projects + 3 yrs production</tspan> into </text>')
    bx = 124 + 520
    p1, w1 = pill(bx, 74, "your-team:main", C["blue_d"], C["blue_t"], size=12)
    p2, w2 = pill(bx + w1 + 44, 74, "ayush:ai-engineer", C["blue_d"], C["blue_t"], size=12)
    body += [p1, f'<text x="{bx + w1 + 10}" y="89" font-size="14" fill="{C["muted"]}">from</text>', p2]
    top = 122
    rh = 44
    box_h = 62 + rh * len(checks) + 92
    body.append(f'<rect x="32" y="{top}" width="{W - 64}" height="{box_h}" rx="10" fill="#fff" stroke="{C["line"]}"/>')
    body.append(f'<rect x="32.5" y="{top + .5}" width="{W - 65}" height="52" rx="10" fill="{C["faint"]}"/>'
                f'<rect x="32.5" y="{top + 40}" width="{W - 65}" height="12" fill="{C["faint"]}"/>'
                f'<line x1="32" y1="{top + 52}" x2="{W - 32}" y2="{top + 52}" stroke="{C["line"]}"/>')
    n = len(checks)
    done_t = .6 + n * .42 + .4
    body.append(f'<g class="hide" style="animation-delay:{done_t:.2f}s"><circle class="spin" cx="58" cy="{top + 26}" r="8" stroke="{C["amber"]}" stroke-width="2.4" stroke-dasharray="34 20"/>'
                f'<text x="78" y="{top + 31}" font-size="14.5" font-weight="600" fill="{C["fg"]}">Some checks haven’t completed yet</text></g>')
    body.append(f'<g class="fi" style="animation-delay:{done_t:.2f}s"><circle cx="58" cy="{top + 26}" r="10" fill="{C["green"]}"/>'
                f'<path d="m53 {top + 26} 3.6 3.6 6.8-7" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<text x="78" y="{top + 31}" font-size="14.5" font-weight="600" fill="{C["fg"]}">All checks have passed</text>'
                f'<text x="{W - 52}" y="{top + 31}" font-size="12.5" fill="{C["muted"]}" text-anchor="end">{n} successful checks</text></g>')
    for i, (name, detail) in enumerate(checks):
        y = top + 52 + i * rh + rh / 2 + 4
        d = .6 + i * .42
        body.append(f'<g class="hide" style="animation-delay:{d + .55:.2f}s"><circle class="spin" cx="58" cy="{y}" r="7" stroke="{C["amber"]}" stroke-width="2.2" stroke-dasharray="26 18"/></g>')
        body.append(f'<g class="pop" style="animation-delay:{d + .55:.2f}s"><path d="m51.5 {y} 4.2 4.2 7.8-8.2" stroke="{C["green"]}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></g>')
        body.append(f'<text class="m" x="84" y="{y + 4.5}" font-size="13" font-weight="600" fill="{C["fg"]}">{esc(name)}</text>')
        body.append(f'<text x="290" y="{y + 4.5}" font-size="13" fill="{C["muted"]}">{esc(detail)}</text>')
        body.append(f'<text class="fi m" style="animation-delay:{d + .55:.2f}s" x="{W - 52}" y="{y + 4.5}" font-size="11.5" fill="{C["green_d"]}" text-anchor="end">passed</text>')
        if i < n - 1:
            body.append(f'<line x1="48" y1="{y + rh / 2 - 4}" x2="{W - 48}" y2="{y + rh / 2 - 4}" stroke="{C["line"]}" stroke-opacity=".7"/>')
    my = top + 52 + rh * n + 4
    body.append(f'<line x1="32" y1="{my}" x2="{W - 32}" y2="{my}" stroke="{C["line"]}"/>')
    body.append(f'<g class="fi" style="animation-delay:{done_t + .2:.2f}s"><circle cx="58" cy="{my + 30}" r="10" fill="{C["green_t"]}" stroke="{C["green"]}"/>'
                f'<path d="m53 {my + 30} 3.6 3.6 6.8-7" stroke="{C["green_d"]}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<text x="78" y="{my + 28}" font-size="14.5" font-weight="600" fill="{C["fg"]}">This branch has no conflicts with the base branch</text>'
                f'<text x="78" y="{my + 48}" font-size="12.5" fill="{C["muted"]}">Based in Coventry, UK · open to roles across the UK</text></g>')
    body.append(f'<g class="fi" style="animation-delay:{done_t + .5:.2f}s"><g class="glow"><rect x="{W - 252}" y="{my + 14}" width="200" height="38" rx="8" fill="{C["green"]}"/>'
                f'<text x="{W - 152}" y="{my + 38}" font-size="14.5" font-weight="600" fill="#fff" text-anchor="middle">Merge pull request</text></g></g>')
    H = top + box_h + 26
    style.append("""
.spin{transform-box:fill-box;transform-origin:center;animation:sp 1s linear infinite}
@keyframes sp{to{transform:rotate(360deg)}}
.hide{animation:hd .01s linear forwards}
@keyframes hd{to{opacity:0;visibility:hidden}}
.pop{opacity:0;transform-box:fill-box;transform-origin:center;animation:pp .4s cubic-bezier(.3,1.6,.5,1) forwards}
@keyframes pp{from{opacity:0;transform:scale(.3)}to{opacity:1;transform:scale(1)}}
.glow{animation:gl 2.6s ease-in-out infinite}
@keyframes gl{0%,100%{opacity:1}50%{opacity:.78}}
""")
    return svg(W, H, "\n".join(body), "".join(style),
               "Pull request: Hire Ayush as your next AI Engineer. All 7 checks passed: DocFlow 91.3% field accuracy from 85.5%, "
               "explainable AI PR-AUC 0.80 from 0.52, LineGuard Hit@5 0.95 from 0.80, 4/4 prompt injections blocked, 131 tests, "
               "3 years production at Cybage, UK Graduate Route.")


# ------------------------------------------------------------------ topics
def topics():
    W = 1000
    groups = [
        ("llms-and-rag", "blue", ["rag", "llm", "langgraph", "langchain", "embeddings", "faiss", "agents", "mcp", "guardrails", "ragas", "prompt-injection-defense"]),
        ("machine-learning", "purple", ["pytorch", "hugging-face", "qlora", "vision-language-models", "document-ai", "lightgbm", "shap", "scikit-learn", "explainable-ai"]),
        ("engineering", "green", ["python", "fastapi", "csharp", "dotnet-core", "rest-api", "sql", "typescript", "odata", "dynamics-365"]),
        ("cloud-and-mlops", "pink", ["aws-sagemaker", "docker", "github-actions", "azure-devops", "mlflow", "ollama", "streamlit", "pytest"]),
    ]
    body = [f'<text x="32" y="44" font-size="17" font-weight="600" fill="{C["fg"]}">Topics</text>',
            f'<text x="{W - 32}" y="44" font-size="12.5" fill="{C["muted"]}" text-anchor="end">what I build with, grouped by area</text>']
    y = 70
    k = 0
    for name, col, items in groups:
        body.append(f'<text class="m" x="32" y="{y + 16}" font-size="11.5" fill="{C[col + "_d"]}">{name}</text>')
        x = 200
        for it in items:
            w = len(it) * 12 * .61 + 22
            if x + w > W - 28:
                y += 32
                x = 200
            p, _ = pill(x, y, it, C[col + "_d"], C[col + "_t"], size=12, cls="fi", delay=.1 + k * .035, pad=11, h=24)
            body.append(p)
            x += w + 8
            k += 1
        y += 44
    H = y + 6
    return svg(W, H, "\n".join(body), "", "Topics: LLMs and RAG, machine learning, engineering, cloud and MLOps")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    for name, fn in [("git-graph", header), ("pull-request", pull_request), ("topics", topics)]:
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
    print("built", sorted(p.name for p in OUT.glob("*.svg")))


if __name__ == "__main__":
    main()
