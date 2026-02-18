"""Public-facing routes."""

from flask import Blueprint, render_template, request

from app.extensions import get_db
from app.data import COMPANIES, COMPANY_LIST

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM services ORDER BY sort_order")
    services = cur.fetchall()
    cur.execute("SELECT * FROM testimonials ORDER BY sort_order")
    testimonials = cur.fetchall()
    cur.execute("SELECT * FROM clients ORDER BY sort_order")
    clients = cur.fetchall()
    cur.execute("SELECT * FROM gallery_items ORDER BY sort_order LIMIT 6")
    gallery = cur.fetchall()
    cur.execute("SELECT * FROM blog_posts WHERE status='published' ORDER BY created_at DESC LIMIT 3")
    latest_posts = cur.fetchall()
    cur.close()
    return render_template(
        "index.html",
        companies=COMPANY_LIST,
        services=services,
        testimonials=testimonials,
        clients=clients,
        gallery=gallery,
        latest_posts=latest_posts,
    )


@public_bp.route("/about")
def about():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM team_members ORDER BY sort_order")
    team = cur.fetchall()
    cur.execute("SELECT * FROM faqs ORDER BY sort_order")
    faqs = cur.fetchall()
    cur.close()
    return render_template("about.html", team=team, faqs=faqs)


@public_bp.route("/services")
def services_page():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM services ORDER BY sort_order")
    services = cur.fetchall()
    cur.close()
    return render_template("services.html", services=services)


@public_bp.route("/gallery")
def gallery_page():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM gallery_items ORDER BY sort_order")
    gallery = cur.fetchall()
    cur.close()
    return render_template("gallery.html", gallery=gallery)


@public_bp.route("/company/<slug>")
def company(slug):
    company_data = COMPANIES.get(slug)
    if not company_data:
        return render_template("404.html"), 404
    return render_template("company.html", company=company_data)


@public_bp.route("/blog")
def blog_list():
    db = get_db()
    cur = db.cursor()
    page = request.args.get("page", 1, type=int)
    per_page = 6
    offset = (page - 1) * per_page
    cur.execute("SELECT COUNT(*) AS c FROM blog_posts WHERE status='published'")
    total = cur.fetchone()["c"]
    cur.execute(
        "SELECT * FROM blog_posts WHERE status='published' ORDER BY created_at DESC LIMIT %s OFFSET %s",
        (per_page, offset),
    )
    posts = cur.fetchall()
    total_pages = max(1, (total + per_page - 1) // per_page)
    cur.close()
    return render_template("blog.html", posts=posts, page=page, total_pages=total_pages)


@public_bp.route("/blog/<slug>")
def blog_detail(slug):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM blog_posts WHERE slug=%s AND status='published'", (slug,))
    post = cur.fetchone()
    if not post:
        cur.close()
        return render_template("404.html"), 404
    cur.execute(
        "SELECT * FROM blog_posts WHERE status='published' AND slug!=%s ORDER BY created_at DESC LIMIT 3",
        (slug,),
    )
    recent = cur.fetchall()
    cur.close()
    return render_template("blog_detail.html", post=post, recent_posts=recent)


@public_bp.route("/contact")
def contact_page():
    return render_template("contact.html")
