# fitlore

> Your training, remembered.

**English | [简体中文](README.zh-CN.md)**

![License](https://img.shields.io/badge/license-MIT-green) ![Python](https://img.shields.io/badge/python-3.8%2B-blue) ![Powered by](https://img.shields.io/badge/charts-ECharts-red)

An AI-agent skill that tracks your workouts and body metrics — built **low-frequency-native** for people who *don't* log every day.

![fitlore dashboard](docs/screenshots/dashboard-top.png)

## Why fitlore

Most fitness trackers quietly assume you'll log every day. You won't. You'll record for two weeks, disappear for three, and come back with a pile of gym-app screenshots.

fitlore doesn't fight that. It's designed around it:

- **Time-independent** — everything compares "this time vs last time", not "this week vs last week". Come back after a month and nothing is broken; a gap is just "not recorded", never a guilt trip.
- **Batch backfill is a first-class citizen** — dump five screenshots and a few voice notes from the past three weeks in one go. fitlore parses them, places them by date, and reviews the whole span as one conversation.
- **Density-adaptive analytics** — dense data gets trend analysis; sparse data gets honest direction-only statements. It never pretends four data points are a trend.
- **Minimal-data first** — weight + training data alone power the full experience. Body fat, sleep, alcohol, nutrition are all optional; missing sections simply hide in charts.

## What you say → what it does

| You say | The agent does |
|:--|:--|
| "Help me set up" / 「帮我建档」 | A progressive interview (only 3 required questions) → your profile + a `fitness-data/` directory |
| Send a gym-app screenshot | Parses exercises, sets × reps × weight, volume → appends to CSVs → reports back |
| "Log these past few days" / 「补录」 | Batch backfill: parses everything, places by date, merges into one review |
| "How have I been doing?" / 「盘一下最近」 | Conversational review since your last one — soreness grading, PR detection, one document |
| "Show my progress" / 「看看我的数据」 | Generates a self-contained HTML dashboard — open it by double-click, no server needed |

## Quickstart

```bash
git clone https://github.com/buuzzy/fitlore.git && mkdir -p ~/.workbuddy/skills && cp -r fitlore ~/.workbuddy/skills/
```

(For Claude Code, copy into `~/.claude/skills/` instead. For a single project, use `<project>/.claude/skills/`.)

Then just say **"help me set up"** (or 「帮我建档」). A few minutes later you have a profile, and your first logged workout can follow immediately.

## How it works

**The skill is the method, your files are the database.** fitlore contains zero personal data — it's all workflow, methodology and chart templates. Your data lives in a `fitness-data/` directory created at runtime:

```
fitness-data/
├── profile.md          # your profile (built during onboarding)
├── measurements.csv    # weigh-ins, body fat, sleep — append-only
├── sessions.csv        # one row per workout session — append-only
├── exercises.csv       # one row per exercise — append-only
├── reviews/            # review documents
└── dashboards/         # generated self-contained HTML reports
```

CSVs are append-only by design: history can't be silently rewritten, corrections go through an auditable "annotate, don't overwrite" rule.

Dashboards are built with one command — `assets/build_dashboard.py` injects your data and the ECharts library into a template, producing a single HTML file (~1MB) that opens anywhere.

## What makes it different

- **Unit & mode comparability rules** — the #1 source of wrong training insights is comparing kg against lbs, or unilateral against bilateral records. fitlore validates comparability before any comparison, PR detection included.
- **"Not recorded ≠ not measured"** — before declaring any dimension "long empty", the skill must ask you once. People usually have the data; they just don't hand it over.
- **No-progress-shaming by default** — unless you explicitly pick strength as your goal, "didn't add weight" is never framed as a failure. Holding weight while cutting is a win.
- **Pain grading baked in** — soreness / tightness / sharp pain / numbness each get a different protocol, checked in every review. Safety red lines outrank every training suggestion.

## Data & privacy

- The skill itself contains **no personal data** — only workflows, rules and templates. Safe to open-source by construction.
- All your data stays in a local `fitness-data/` directory. Nothing goes to any third party.
- Requirements: any AI-agent environment with file access and Python 3.8+ (standard library only). Charts are powered by [Apache ECharts](https://echarts.apache.org/), pre-embedded into every generated report — end users install nothing.

## Repository map

```
fitlore/
├── SKILL.md                      # entry point: triggers, state machine, core principles
├── references/                   # onboarding · data collection · review workflow · analysis rules · visualization
├── assets/
│   ├── dashboard-template.html   # ECharts report template
│   ├── build_dashboard.py        # one-command dashboard builder
│   └── echarts.min.js            # Apache ECharts 5 (Apache-2.0)
├── examples/
│   ├── data-demo.json            # fictional demo user
│   ├── dashboard-demo.html       # generated demo report — double-click to preview
│   └── scenarios/                # four-density demo: 1 day / 1 week / 1 month / sparse
│                                 #   → open scenarios/index.html to switch between them
├── docs/screenshots/             # images used in this README
├── CHANGELOG.md
└── LICENSE
```

## License

MIT — see [LICENSE](LICENSE).
