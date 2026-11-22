# Portfolio

A simple Flask site. All content lives in two YAML files — no HTML editing needed.

## Run locally

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py
```

Open http://127.0.0.1:5000. Edits to `content/*.yaml` show up on refresh.

## Add a project

Each project is one Markdown file in `content/projects/`. The file name becomes the page address
(`word-ladder.md` is shown at `/projects/word-ladder/`). Copy an existing file and edit it:

```markdown
---
title: My New Project
description: One or two sentences. Shown on the card and at the top of the project page.
tags: [Python, FastAPI]
github: https://github.com/you/repo   # optional
demo: https://...                     # optional
date: 2026-11                         # shown as "November 2026"; newest first
---

## What it does

Write the full project page here in Markdown: headings, lists, code blocks and tables all work.
```

If a required field is missing, the page shows a clear error naming the file.

## Edit your details

Everything else (name, intro, about, skills, experience, contact links, résumé) is in `content/profile.yaml`.

## Publish as a static site

```bash
.venv/bin/python freeze.py
```

This writes plain HTML to `build/`, which you can upload to GitHub Pages or Netlify.

## Hosting

The site is on GitHub Pages. Every push to `main` runs `.github/workflows/deploy.yml`, which
builds the site with `freeze.py` and publishes it, so to update the live site just edit, commit and push.
