from flask import Flask, render_template, send_from_directory, Response, request
from datetime import datetime

app = Flask(__name__)


# ========== PERFORMANCE: Static asset caching ==========
@app.after_request
def add_headers(response):
    """Add caching and security headers to all responses."""
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    # Cache static assets aggressively (CSS, JS, images)
    if request.path.startswith("/static/"):
        # Cache static files for 1 year (immutable content)
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    else:
        # HTML pages: disable caching to force updates
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "-1"

    return response


@app.route("/")
def index():
    return render_template("index.html", active_page="home")


@app.route("/about")
def about():
    return render_template("about.html", active_page="about")


@app.route("/skills")
def skills():
    return render_template("skills.html", active_page="skills")


@app.route("/projects")
def projects():
    return render_template("projects.html", active_page="projects")


@app.route("/contact")
def contact():
    return render_template("contact.html", active_page="contact")


@app.route("/robots.txt")
def robots():
    return send_from_directory(app.static_folder, "robots.txt")


@app.route("/sitemap.xml")
def sitemap():
    pages = [
        {"loc": "https://buildwithsamrudh.xyz/", "priority": "1.0", "changefreq": "weekly"},
        {"loc": "https://buildwithsamrudh.xyz/about", "priority": "0.8", "changefreq": "monthly"},
        {"loc": "https://buildwithsamrudh.xyz/skills", "priority": "0.7", "changefreq": "monthly"},
        {"loc": "https://buildwithsamrudh.xyz/projects", "priority": "0.9", "changefreq": "weekly"},
        {"loc": "https://buildwithsamrudh.xyz/contact", "priority": "0.6", "changefreq": "yearly"},
    ]
    today = datetime.now().strftime("%Y-%m-%d")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for p in pages:
        xml += f'  <url>\n'
        xml += f'    <loc>{p["loc"]}</loc>\n'
        xml += f'    <lastmod>{today}</lastmod>\n'
        xml += f'    <changefreq>{p["changefreq"]}</changefreq>\n'
        xml += f'    <priority>{p["priority"]}</priority>\n'
        xml += f'  </url>\n'
    xml += '</urlset>'
    return Response(xml, mimetype="application/xml",
                    headers={"Cache-Control": "public, max-age=86400"})


if __name__ == "__main__":
    app.run(debug=True)
