"""Export the site to plain HTML in build/ for static hosting (GitHub Pages, Netlify)."""
from flask_frozen import Freezer

from app import app

app.config["FREEZER_DESTINATION"] = "build"
app.config["FREEZER_RELATIVE_URLS"] = True

freezer = Freezer(app)

if __name__ == "__main__":
    freezer.freeze()
    print("Built site into build/ — open build/index.html to check it.")
