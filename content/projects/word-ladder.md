---
title: Word Ladder
description: >-
  A word game where you change one letter at a time to turn one word into
  another. Play solo, team up with a friend, race each other, or take on the
  daily puzzle.
tags: [Python, FastAPI, SQLAlchemy, PostgreSQL, WebSockets, Web Push, PWA, pytest]
github: https://github.com/aayushi-nimbly/wordLadder
demo: https://wordladder-ys5c.onrender.com
date: 2026-11
---

## What it does

- **Four ways to play.** Solo; Team, where two players take turns on one shared ladder and win together; Compete, where both players climb their own ladder for the same puzzle and fewest steps wins, then fastest time; and Daily, one puzzle a day for everyone with leaderboards for today, this week and friends.
- **Puzzles at the right difficulty.** Easy, medium and hard puzzles in 4, 5 and 6 letter words, or your own start and end words.
- **Play with a friend by link.** Moves show up live when you're both in the game, and it switches to turn by turn when you're not.
- **Phone notifications.** "Your turn", "friend joined", and a reminder if a turn has waited 24 hours.
- **Installable.** Sign in with Google and add it to your home screen as an app.

An example ladder, 4 moves from COLD to WARM:

```
COLD → CORD → CARD → WARD → WARM
```

## How it works

### The word graph

Every valid word of a given length is a node, and two words are linked when they differ by exactly one letter. Comparing every pair of words would be slow, so the graph is built by bucketing words under wildcard patterns: "cold" goes into `_old`, `c_ld`, `co_d` and `col_`, and every word in the same bucket is a neighbour. A breadth-first search from any word then gives the shortest number of moves to every other word, and those results are cached.

### Picking fair puzzles

Each word length has three word lists:

- **valid:** every word in the public-domain ENABLE list. Any of these is accepted as a move.
- **known:** valid words most people recognise. Hints and solutions use these.
- **common:** everyday words. Only these are suggested as start and end words.

A puzzle is only suggested if its shortest ladder can be made entirely from known words, and that shortest length (the par) falls in the range for the chosen difficulty. So a player is never expected to know an obscure word to reach par, and every hint points one step along that shortest path.

### Live games

A small WebSocket hub keeps every open connection for each game, per player, and pushes the fresh game state to both players after every change. It also tracks whether each tab is actually on screen, so a player with the game open in a background tab or on a locked phone still gets a notification.

### Fair rankings

In Compete and Daily, each hint adds a step to your score, and results are ranked by fewest steps, then fastest time. The daily puzzle and its word length are picked from the date (India time), so everyone gets the same puzzle and one attempt at it.

## Shipping it

The backend is FastAPI with SQLAlchemy, running on SQLite locally and Postgres in production. It's hosted on Render's free plan with the database on Neon, both in Singapore to keep them close to players in India. Every push to `main` redeploys, and a `/healthz` endpoint backs Render's health check.

Notifications use Web Push, signed with a key pair derived from a secret set in the environment. A pytest suite covers the word engine, races, the daily puzzle, accounts, notifications and the API, and can run against Postgres as well as SQLite.

## Known limitations

- On the free plan the app sleeps after 15 minutes without visitors, so the first visit after that takes about a minute.
- Turn reminders are only checked while the app is awake.
- On iPhone, notifications only work after adding the app to the Home Screen (iOS 16.4+).
