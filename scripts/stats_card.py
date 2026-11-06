#!/usr/bin/env python3
"""Builds dist/stats.svg from the GitHub GraphQL API. Standard library only.

Runs in the same workflow as the snake, so the README does not depend on a
public stats service staying online.

    GITHUB_TOKEN=... python3 scripts/stats_card.py <login> dist/stats.svg
"""
import json
import os
import sys
import urllib.request
from collections import Counter
from datetime import date
from html import escape
from pathlib import Path

# Markup and build files say little about what someone writes day to day, and
# notebook size is mostly embedded cell output, which would swamp every real language.
IGNORED = {"HTML", "CSS", "SCSS", "Mako", "Dockerfile", "Makefile", "Batchfile", "Procfile", "Pug", "Jupyter Notebook"}
TOP_N = 5

BG, PANEL, RULE = "#0b0e1f", "#141a35", "#2f3a78"
INK, MUTED, BAR = "#f4f1ff", "#a3a6c9", "#5ee7ff"
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

QUERY = """
query($login: String!, $after: String) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount date } }
      }
    }
    repositories(first: 100, after: $after, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes { languages(first: 20, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } } }
    }
  }
}
"""


def gql(token, **variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "profile-stats-card"},
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        body = json.load(res)
    if body.get("errors"):
        raise SystemExit(f"GraphQL error: {body['errors']}")
    return body["data"]["user"]


def collect(token, login):
    user = gql(token, login=login, after=None)
    calendar = user["contributionsCollection"]["contributionCalendar"]
    repos = user["repositories"]
    langs = Counter()
    while True:
        for repo in repos["nodes"]:
            for edge in repo["languages"]["edges"]:
                if edge["node"]["name"] not in IGNORED:
                    langs[edge["node"]["name"]] += edge["size"]
        if not repos["pageInfo"]["hasNextPage"]:
            break
        repos = gql(token, login=login, after=repos["pageInfo"]["endCursor"])["repositories"]

    days = [d for week in calendar["weeks"] for d in week["contributionDays"]]
    days = [d for d in days if date.fromisoformat(d["date"]) <= date.today()]
    longest = run = 0
    for day in days:
        run = run + 1 if day["contributionCount"] else 0
        longest = max(longest, run)
    return {
        "contributions": calendar["totalContributions"],
        "active_days": sum(1 for d in days if d["contributionCount"]),
        "longest_streak": longest,
        "repos": user["repositories"]["totalCount"],
        "langs": langs,
    }


def tile(x, y, value, label):
    return f"""
  <rect x="{x}" y="{y}" width="196" height="92" rx="8" fill="{PANEL}" stroke="{RULE}"/>
  <text x="{x + 16}" y="{y + 46}" font-size="32" font-weight="700" fill="{INK}">{value}</text>
  <text x="{x + 16}" y="{y + 72}" font-size="13" fill="{MUTED}">{escape(label)}</text>"""


def render(s):
    total = sum(s["langs"].values()) or 1
    top = s["langs"].most_common(TOP_N)
    peak = top[0][1] if top else 1
    bars, x0, track = [], 568, 270
    for i, (name, size) in enumerate(top):
        y = 76 + i * 28
        w = max(4, round(size / peak * track))
        bars.append(f"""
  <text x="{x0 - 12}" y="{y + 9}" font-size="13" fill="{INK}" text-anchor="end">{escape(name)}</text>
  <rect class="bar" style="animation-delay:{i * 90}ms" x="{x0}" y="{y}" width="{w}" height="10" rx="4" fill="{BAR}"/>
  <text x="{x0 + track + 12}" y="{y + 9}" font-size="13" fill="{MUTED}">{size / total * 100:.1f}%</text>""")

    tiles = "".join((
        tile(32, 60, s["contributions"], "contributions, 1 year"),
        tile(240, 60, s["repos"], "public repositories"),
        tile(32, 164, s["active_days"], "active days, 1 year"),
        tile(240, 164, s["longest_streak"], "longest streak, days"),
    ))
    summary = ", ".join(f"{n} {v / total * 100:.0f}%" for n, v in top)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="960" height="280" viewBox="0 0 960 280" role="img" aria-labelledby="t d" font-family="{FONT}">
  <title id="t">GitHub activity and top languages</title>
  <desc id="d">{s['contributions']} contributions and {s['active_days']} active days in 12 months, {s['repos']} public repositories, longest streak {s['longest_streak']} days. Top languages by code size: {escape(summary)}.</desc>
  <style>
    .bar {{ transform-box: fill-box; transform-origin: left; animation: grow .9s cubic-bezier(.2,.8,.2,1) both; }}
    @keyframes grow {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
    @media (prefers-reduced-motion: reduce) {{ .bar {{ animation: none; }} }}
  </style>
  <rect width="960" height="280" rx="12" fill="{BG}"/>
  <text x="32" y="38" font-size="15" font-weight="700" fill="{INK}">Activity</text>
  <text x="456" y="38" font-size="15" font-weight="700" fill="{INK}">Top languages</text>
  <text x="928" y="38" font-size="12" fill="{MUTED}" text-anchor="end">share of code in public repos</text>{tiles}{''.join(bars)}
</svg>
"""


def main():
    login = sys.argv[1] if len(sys.argv) > 1 else os.environ["GITHUB_REPOSITORY_OWNER"]
    out = Path(sys.argv[2] if len(sys.argv) > 2 else "dist/stats.svg")
    stats = collect(os.environ["GITHUB_TOKEN"], login)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(stats), encoding="utf-8")
    print({k: v for k, v in stats.items() if k != "langs"}, stats["langs"].most_common(TOP_N))


if __name__ == "__main__":
    main()
