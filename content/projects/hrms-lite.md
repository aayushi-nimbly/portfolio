---
title: HRMS Lite
description: >-
  A lightweight HR management system for keeping employee records and marking
  daily attendance, with a Django REST API backend and a React frontend.
tags: [Python, Django, Django REST Framework, PostgreSQL, React, Vite]
github: https://github.com/aayushi-nimbly/hrms
demo: https://hrms-indol-ten.vercel.app
date: 2026-02
---

## What it does

- **Employee records.** Add, list and remove employees, each with a unique employee ID and email, a name and a department.
- **Daily attendance.** Mark an employee present or absent for a day. Marking the same day again updates the record instead of creating a duplicate.
- **Dashboard.** Total employees, plus how many were present and absent on any date (today by default).
- **History.** Attendance for one employee or for everyone, filterable by date.

## How it works

### Data model

Two tables: `Employee` and `Attendance`, linked by a foreign key. Attendance has a unique constraint on `(employee, date)`, so the database itself guarantees one record per employee per day, not just the application code.

### API

| Method | Endpoint | What it does |
| --- | --- | --- |
| GET, POST | `/api/employees/` | List employees, or add one |
| DELETE | `/api/employees/<id>/` | Remove an employee and their attendance |
| GET | `/api/employees/<id>/attendance/` | One employee's attendance, optional `?date=` |
| POST | `/api/attendance/` | Mark attendance (creates or updates) |
| GET | `/api/attendance/all/` | Everyone's attendance, optional `?date=` |
| GET | `/api/dashboard/` | Totals and present/absent counts for a date |

### Implementation details

- **Generic views.** The API is built on Django REST Framework's generic views, so each endpoint is a few lines.
- **Validation in one place.** A separate serializer for marking attendance checks that the employee ID exists and does a create-or-update, so the endpoint can be called safely more than once.
- **No N+1 queries.** Attendance lists use `select_related` to fetch employee names in the same query.

## Shipping it

The backend runs on Render with gunicorn and Postgres, and uses SQLite locally. The React frontend is built with Vite and deployed on Vercel, pointing at the API through an environment variable.
