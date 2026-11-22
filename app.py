"""Portfolio site: renders content/profile.yaml and content/projects/*.md into HTML pages."""
from datetime import date, datetime
from pathlib import Path

import markdown
import yaml
from flask import Flask, abort, render_template

BASE_DIR = Path(__file__).parent
CONTENT_DIR = BASE_DIR / "content"
PROJECTS_DIR = CONTENT_DIR / "projects"

REQUIRED_PROFILE_FIELDS = ["name", "headline", "intro", "email"]
REQUIRED_PROJECT_FIELDS = ["title", "description"]

app = Flask(__name__)


class ContentError(Exception):
    """Raised when a content file is missing fields or malformed."""


def read_yaml(filename):
    path = CONTENT_DIR / filename
    try:
        with path.open(encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        raise ContentError(f"{filename} is not valid YAML:\n{e}") from e


def load_profile():
    profile = read_yaml("profile.yaml")
    missing = [f for f in REQUIRED_PROFILE_FIELDS if not profile.get(f)]
    if missing:
        raise ContentError(f"profile.yaml is missing: {', '.join(missing)}")
    profile.setdefault("skills", {})
    if not isinstance(profile["skills"], dict):
        raise ContentError("profile.yaml: skills must be categories, e.g. 'Languages: [Python, SQL]'")
    profile.setdefault("experience", [])
    profile.setdefault("links", {})
    return profile


def read_project(path):
    """A project file is YAML details between --- lines, then the write-up in Markdown."""
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if not text.startswith("---") or len(parts) < 3:
        raise ContentError(f"projects/{path.name} must start with details between two '---' lines")
    try:
        project = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as e:
        raise ContentError(f"projects/{path.name} has invalid details:\n{e}") from e

    missing = [f for f in REQUIRED_PROJECT_FIELDS if not project.get(f)]
    if missing:
        raise ContentError(f"projects/{path.name} is missing: {', '.join(missing)}")
    project["slug"] = path.stem
    project.setdefault("tags", [])
    project["date"] = str(project.get("date", ""))
    project["body"] = markdown.markdown(parts[2], extensions=["fenced_code", "tables"])
    return project


def load_projects():
    projects = [read_project(path) for path in PROJECTS_DIR.glob("*.md")]
    # Newest first.
    projects.sort(key=lambda p: p["date"], reverse=True)
    return projects


@app.template_filter("month_year")
def month_year(value):
    """'2026-11' -> 'November 2026'. Anything else is shown as written."""
    try:
        return datetime.strptime(value[:7], "%Y-%m").strftime("%B %Y")
    except ValueError:
        return value


@app.route("/")
def index():
    return render_template(
        "index.html",
        profile=load_profile(),
        projects=load_projects(),
        year=date.today().year,
    )


@app.route("/projects/<slug>/")
def project(slug):
    project = next((p for p in load_projects() if p["slug"] == slug), None)
    if project is None:
        abort(404)
    return render_template(
        "project.html",
        profile=load_profile(),
        project=project,
        year=date.today().year,
    )


@app.errorhandler(ContentError)
def content_error(e):
    return f"<h2>Content error</h2><pre>{e}</pre>", 500


if __name__ == "__main__":
    app.run(debug=True)
