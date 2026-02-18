"""Admin dashboard routes."""

import hashlib
from functools import wraps

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)

from app.extensions import get_db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Silakan login terlebih dahulu.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

@admin_bp.route("/")
@login_required
def dashboard():
    db = get_db()
    cur = db.cursor()
    tables = ["blog_posts", "services", "gallery_items", "testimonials", "clients", "team_members", "faqs"]
    keys = ["posts", "services", "gallery", "testimonials", "clients", "team", "faqs"]
    stats = {}
    for key, table in zip(keys, tables):
        cur.execute(f"SELECT COUNT(*) AS c FROM {table}")
        stats[key] = cur.fetchone()["c"]
    cur.execute("SELECT * FROM blog_posts ORDER BY created_at DESC LIMIT 5")
    recent_posts = cur.fetchall()
    cur.close()
    return render_template("admin/dashboard.html", stats=stats, recent_posts=recent_posts)


# ---------------------------------------------------------------------------
# Blog CRUD
# ---------------------------------------------------------------------------

@admin_bp.route("/blog")
@login_required
def blog_list():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM blog_posts ORDER BY created_at DESC")
    posts = cur.fetchall()
    cur.close()
    return render_template("admin/blog_list.html", posts=posts)


@admin_bp.route("/blog/create", methods=["GET", "POST"])
@login_required
def blog_create():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        slug = request.form.get("slug", "").strip() or title.lower().replace(" ", "-")
        slug = "".join(c if c.isalnum() or c == "-" else "-" for c in slug).strip("-")
        excerpt = request.form.get("excerpt", "").strip()
        content = request.form.get("content", "").strip()
        category = request.form.get("category", "Umum").strip()
        image_url = request.form.get("image_url", "").strip()
        cover_icon = request.form.get("cover_icon", "bx-news").strip()
        cover_gradient = request.form.get("cover_gradient", "from-purple-600 to-blue-600").strip()
        status = request.form.get("status", "published")
        author = session.get("username", "Admin")
        db = get_db()
        cur = db.cursor()
        try:
            cur.execute(
                "INSERT INTO blog_posts (title, slug, excerpt, content, image_url, cover_icon, cover_gradient, category, author, status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (title, slug, excerpt, content, image_url, cover_icon, cover_gradient, category, author, status),
            )
            db.commit()
            flash("Blog post berhasil dibuat!", "success")
            return redirect(url_for("admin.blog_list"))
        except Exception:
            db.rollback()
            flash("Slug sudah digunakan.", "error")
        finally:
            cur.close()
    return render_template("admin/blog_form.html", post=None)


@admin_bp.route("/blog/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def blog_edit(post_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM blog_posts WHERE id=%s", (post_id,))
    post = cur.fetchone()
    if not post:
        cur.close()
        flash("Post tidak ditemukan.", "error")
        return redirect(url_for("admin.blog_list"))
    if request.method == "POST":
        try:
            cur.execute(
                "UPDATE blog_posts SET title=%s, slug=%s, excerpt=%s, content=%s, image_url=%s, cover_icon=%s, cover_gradient=%s, category=%s, status=%s WHERE id=%s",
                (
                    request.form["title"].strip(),
                    request.form["slug"].strip(),
                    request.form.get("excerpt", "").strip(),
                    request.form["content"].strip(),
                    request.form.get("image_url", "").strip(),
                    request.form.get("cover_icon", "bx-news").strip(),
                    request.form.get("cover_gradient", "from-purple-600 to-blue-600").strip(),
                    request.form.get("category", "Umum").strip(),
                    request.form.get("status", "published"),
                    post_id,
                ),
            )
            db.commit()
            flash("Blog post berhasil diperbarui!", "success")
            return redirect(url_for("admin.blog_list"))
        except Exception:
            db.rollback()
            flash("Slug sudah digunakan.", "error")
    cur.close()
    return render_template("admin/blog_form.html", post=post)


@admin_bp.route("/blog/<int:post_id>/delete", methods=["POST"])
@login_required
def blog_delete(post_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM blog_posts WHERE id=%s", (post_id,))
    db.commit()
    cur.close()
    flash("Blog post berhasil dihapus.", "success")
    return redirect(url_for("admin.blog_list"))


# ---------------------------------------------------------------------------
# Services CRUD
# ---------------------------------------------------------------------------

@admin_bp.route("/services")
@login_required
def services_list():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM services ORDER BY sort_order")
    services = cur.fetchall()
    cur.close()
    return render_template("admin/services_list.html", services=services)


@admin_bp.route("/services/create", methods=["GET", "POST"])
@login_required
def service_create():
    if request.method == "POST":
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO services (icon, title, description, image_url, gradient, sort_order) VALUES (%s,%s,%s,%s,%s,%s)",
            (request.form["icon"], request.form["title"], request.form["description"], request.form.get("image_url", ""), request.form["gradient"], request.form.get("sort_order", 0, type=int)),
        )
        db.commit()
        cur.close()
        flash("Layanan berhasil ditambahkan!", "success")
        return redirect(url_for("admin.services_list"))
    return render_template("admin/service_form.html", service=None)


@admin_bp.route("/services/<int:sid>/edit", methods=["GET", "POST"])
@login_required
def service_edit(sid):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM services WHERE id=%s", (sid,))
    service = cur.fetchone()
    if not service:
        cur.close()
        flash("Layanan tidak ditemukan.", "error")
        return redirect(url_for("admin.services_list"))
    if request.method == "POST":
        cur.execute(
            "UPDATE services SET icon=%s, title=%s, description=%s, image_url=%s, gradient=%s, sort_order=%s WHERE id=%s",
            (request.form["icon"], request.form["title"], request.form["description"], request.form.get("image_url", ""), request.form["gradient"], request.form.get("sort_order", 0, type=int), sid),
        )
        db.commit()
        flash("Layanan berhasil diperbarui!", "success")
        cur.close()
        return redirect(url_for("admin.services_list"))
    cur.close()
    return render_template("admin/service_form.html", service=service)


@admin_bp.route("/services/<int:sid>/delete", methods=["POST"])
@login_required
def service_delete(sid):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM services WHERE id=%s", (sid,))
    db.commit()
    cur.close()
    flash("Layanan berhasil dihapus.", "success")
    return redirect(url_for("admin.services_list"))


# ---------------------------------------------------------------------------
# Testimonials CRUD
# ---------------------------------------------------------------------------

@admin_bp.route("/testimonials")
@login_required
def testimonials():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM testimonials ORDER BY sort_order")
    items = cur.fetchall()
    cur.close()
    return render_template("admin/testimonials_list.html", items=items)


@admin_bp.route("/testimonials/create", methods=["GET", "POST"])
@login_required
def testimonial_create():
    if request.method == "POST":
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO testimonials (name, position, company, content, rating, avatar_gradient, sort_order) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (request.form["name"], request.form["position"], request.form["company"], request.form["content"],
             request.form.get("rating", 5, type=int), request.form.get("avatar_gradient", "from-purple-500 to-blue-500"), request.form.get("sort_order", 0, type=int)),
        )
        db.commit()
        cur.close()
        flash("Testimoni berhasil ditambahkan!", "success")
        return redirect(url_for("admin.testimonials"))
    return render_template("admin/testimonial_form.html", item=None)


@admin_bp.route("/testimonials/<int:tid>/edit", methods=["GET", "POST"])
@login_required
def testimonial_edit(tid):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM testimonials WHERE id=%s", (tid,))
    item = cur.fetchone()
    if not item:
        cur.close()
        flash("Testimoni tidak ditemukan.", "error")
        return redirect(url_for("admin.testimonials"))
    if request.method == "POST":
        cur.execute(
            "UPDATE testimonials SET name=%s, position=%s, company=%s, content=%s, rating=%s, avatar_gradient=%s, sort_order=%s WHERE id=%s",
            (request.form["name"], request.form["position"], request.form["company"], request.form["content"],
             request.form.get("rating", 5, type=int), request.form.get("avatar_gradient", "from-purple-500 to-blue-500"), request.form.get("sort_order", 0, type=int), tid),
        )
        db.commit()
        flash("Testimoni berhasil diperbarui!", "success")
        cur.close()
        return redirect(url_for("admin.testimonials"))
    cur.close()
    return render_template("admin/testimonial_form.html", item=item)


@admin_bp.route("/testimonials/<int:tid>/delete", methods=["POST"])
@login_required
def testimonial_delete(tid):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM testimonials WHERE id=%s", (tid,))
    db.commit()
    cur.close()
    flash("Testimoni berhasil dihapus.", "success")
    return redirect(url_for("admin.testimonials"))


# ---------------------------------------------------------------------------
# Gallery CRUD
# ---------------------------------------------------------------------------

@admin_bp.route("/gallery")
@login_required
def gallery():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM gallery_items ORDER BY sort_order")
    items = cur.fetchall()
    cur.close()
    return render_template("admin/gallery_list.html", items=items)


@admin_bp.route("/gallery/create", methods=["GET", "POST"])
@login_required
def gallery_create():
    if request.method == "POST":
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO gallery_items (title, company, category, image_url, icon, gradient, sort_order) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (request.form["title"], request.form["company"], request.form["category"], request.form.get("image_url", ""), request.form.get("icon", "bx-building"), request.form.get("gradient", "from-purple-600 to-blue-600"), request.form.get("sort_order", 0, type=int)),
        )
        db.commit()
        cur.close()
        flash("Item galeri berhasil ditambahkan!", "success")
        return redirect(url_for("admin.gallery"))
    return render_template("admin/gallery_form.html", item=None)


@admin_bp.route("/gallery/<int:gid>/edit", methods=["GET", "POST"])
@login_required
def gallery_edit(gid):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM gallery_items WHERE id=%s", (gid,))
    item = cur.fetchone()
    if not item:
        cur.close()
        flash("Item tidak ditemukan.", "error")
        return redirect(url_for("admin.gallery"))
    if request.method == "POST":
        cur.execute(
            "UPDATE gallery_items SET title=%s, company=%s, category=%s, image_url=%s, icon=%s, gradient=%s, sort_order=%s WHERE id=%s",
            (request.form["title"], request.form["company"], request.form["category"], request.form.get("image_url", ""), request.form.get("icon", "bx-building"), request.form.get("gradient", "from-purple-600 to-blue-600"), request.form.get("sort_order", 0, type=int), gid),
        )
        db.commit()
        flash("Item galeri berhasil diperbarui!", "success")
        cur.close()
        return redirect(url_for("admin.gallery"))
    cur.close()
    return render_template("admin/gallery_form.html", item=item)


@admin_bp.route("/gallery/<int:gid>/delete", methods=["POST"])
@login_required
def gallery_delete(gid):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM gallery_items WHERE id=%s", (gid,))
    db.commit()
    cur.close()
    flash("Item galeri berhasil dihapus.", "success")
    return redirect(url_for("admin.gallery"))


# ---------------------------------------------------------------------------
# Team CRUD
# ---------------------------------------------------------------------------

@admin_bp.route("/team")
@login_required
def team():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM team_members ORDER BY sort_order")
    items = cur.fetchall()
    cur.close()
    return render_template("admin/team_list.html", items=items)


@admin_bp.route("/team/create", methods=["GET", "POST"])
@login_required
def team_create():
    if request.method == "POST":
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO team_members (name, position, bio, image_url, icon, gradient, sort_order) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (request.form["name"], request.form["position"], request.form["bio"], request.form.get("image_url", ""), request.form.get("icon", "bx-user-circle"), request.form.get("gradient", "from-purple-500 to-blue-500"), request.form.get("sort_order", 0, type=int)),
        )
        db.commit()
        cur.close()
        flash("Anggota tim berhasil ditambahkan!", "success")
        return redirect(url_for("admin.team"))
    return render_template("admin/team_form.html", item=None)


@admin_bp.route("/team/<int:tid>/edit", methods=["GET", "POST"])
@login_required
def team_edit(tid):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM team_members WHERE id=%s", (tid,))
    item = cur.fetchone()
    if not item:
        cur.close()
        flash("Anggota tim tidak ditemukan.", "error")
        return redirect(url_for("admin.team"))
    if request.method == "POST":
        cur.execute(
            "UPDATE team_members SET name=%s, position=%s, bio=%s, image_url=%s, icon=%s, gradient=%s, sort_order=%s WHERE id=%s",
            (request.form["name"], request.form["position"], request.form["bio"], request.form.get("image_url", ""), request.form.get("icon", "bx-user-circle"), request.form.get("gradient", "from-purple-500 to-blue-500"), request.form.get("sort_order", 0, type=int), tid),
        )
        db.commit()
        flash("Anggota tim berhasil diperbarui!", "success")
        cur.close()
        return redirect(url_for("admin.team"))
    cur.close()
    return render_template("admin/team_form.html", item=item)


@admin_bp.route("/team/<int:tid>/delete", methods=["POST"])
@login_required
def team_delete(tid):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM team_members WHERE id=%s", (tid,))
    db.commit()
    cur.close()
    flash("Anggota tim berhasil dihapus.", "success")
    return redirect(url_for("admin.team"))


# ---------------------------------------------------------------------------
# FAQ CRUD
# ---------------------------------------------------------------------------

@admin_bp.route("/faqs")
@login_required
def faqs():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM faqs ORDER BY sort_order")
    items = cur.fetchall()
    cur.close()
    return render_template("admin/faq_list.html", items=items)


@admin_bp.route("/faqs/create", methods=["GET", "POST"])
@login_required
def faq_create():
    if request.method == "POST":
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO faqs (question, answer, sort_order) VALUES (%s,%s,%s)",
            (request.form["question"], request.form["answer"], request.form.get("sort_order", 0, type=int)),
        )
        db.commit()
        cur.close()
        flash("FAQ berhasil ditambahkan!", "success")
        return redirect(url_for("admin.faqs"))
    return render_template("admin/faq_form.html", item=None)


@admin_bp.route("/faqs/<int:fid>/edit", methods=["GET", "POST"])
@login_required
def faq_edit(fid):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM faqs WHERE id=%s", (fid,))
    item = cur.fetchone()
    if not item:
        cur.close()
        flash("FAQ tidak ditemukan.", "error")
        return redirect(url_for("admin.faqs"))
    if request.method == "POST":
        cur.execute(
            "UPDATE faqs SET question=%s, answer=%s, sort_order=%s WHERE id=%s",
            (request.form["question"], request.form["answer"], request.form.get("sort_order", 0, type=int), fid),
        )
        db.commit()
        flash("FAQ berhasil diperbarui!", "success")
        cur.close()
        return redirect(url_for("admin.faqs"))
    cur.close()
    return render_template("admin/faq_form.html", item=item)


@admin_bp.route("/faqs/<int:fid>/delete", methods=["POST"])
@login_required
def faq_delete(fid):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM faqs WHERE id=%s", (fid,))
    db.commit()
    cur.close()
    flash("FAQ berhasil dihapus.", "success")
    return redirect(url_for("admin.faqs"))


# ---------------------------------------------------------------------------
# Clients CRUD
# ---------------------------------------------------------------------------

@admin_bp.route("/clients")
@login_required
def clients():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM clients ORDER BY sort_order")
    items = cur.fetchall()
    cur.close()
    return render_template("admin/client_list.html", items=items)


@admin_bp.route("/clients/create", methods=["GET", "POST"])
@login_required
def client_create():
    if request.method == "POST":
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO clients (name, icon, sort_order) VALUES (%s,%s,%s)",
            (request.form["name"], request.form.get("icon", "bx-building"), request.form.get("sort_order", 0, type=int)),
        )
        db.commit()
        cur.close()
        flash("Klien berhasil ditambahkan!", "success")
        return redirect(url_for("admin.clients"))
    return render_template("admin/client_form.html", item=None)


@admin_bp.route("/clients/<int:cid>/edit", methods=["GET", "POST"])
@login_required
def client_edit(cid):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM clients WHERE id=%s", (cid,))
    item = cur.fetchone()
    if not item:
        cur.close()
        flash("Klien tidak ditemukan.", "error")
        return redirect(url_for("admin.clients"))
    if request.method == "POST":
        cur.execute(
            "UPDATE clients SET name=%s, icon=%s, sort_order=%s WHERE id=%s",
            (request.form["name"], request.form.get("icon", "bx-building"), request.form.get("sort_order", 0, type=int), cid),
        )
        db.commit()
        flash("Klien berhasil diperbarui!", "success")
        cur.close()
        return redirect(url_for("admin.clients"))
    cur.close()
    return render_template("admin/client_form.html", item=item)


@admin_bp.route("/clients/<int:cid>/delete", methods=["POST"])
@login_required
def client_delete(cid):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM clients WHERE id=%s", (cid,))
    db.commit()
    cur.close()
    flash("Klien berhasil dihapus.", "success")
    return redirect(url_for("admin.clients"))


# ---------------------------------------------------------------------------
# Change password
# ---------------------------------------------------------------------------

@admin_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        current = request.form.get("current_password", "")
        new_pw = request.form.get("new_password", "")
        confirm = request.form.get("confirm_password", "")
        if new_pw != confirm:
            flash("Password baru tidak cocok.", "error")
        elif len(new_pw) < 6:
            flash("Password minimal 6 karakter.", "error")
        else:
            db = get_db()
            cur = db.cursor()
            current_hash = hashlib.sha256(current.encode()).hexdigest()
            cur.execute(
                "SELECT * FROM users WHERE id=%s AND password_hash=%s",
                (session["user_id"], current_hash),
            )
            user = cur.fetchone()
            if not user:
                flash("Password lama salah.", "error")
            else:
                new_hash = hashlib.sha256(new_pw.encode()).hexdigest()
                cur.execute("UPDATE users SET password_hash=%s WHERE id=%s", (new_hash, session["user_id"]))
                db.commit()
                flash("Password berhasil diubah!", "success")
                cur.close()
                return redirect(url_for("admin.dashboard"))
            cur.close()
    return render_template("admin/change_password.html")


# ---------------------------------------------------------------------------
# Site Settings
# ---------------------------------------------------------------------------

@admin_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    db = get_db()
    cur = db.cursor()
    if request.method == "POST":
        for key in ("app_name", "logo_url", "tagline"):
            val = request.form.get(key, "").strip()
            cur.execute(
                "INSERT INTO site_settings (setting_key, setting_value) VALUES (%s, %s) "
                "ON DUPLICATE KEY UPDATE setting_value=%s",
                (key, val, val),
            )
        db.commit()
        flash("Pengaturan berhasil disimpan!", "success")
        return redirect(url_for("admin.settings"))
    cur.execute("SELECT setting_key, setting_value FROM site_settings")
    rows = cur.fetchall()
    cur.close()
    current = {r["setting_key"]: r["setting_value"] for r in rows}
    return render_template("admin/settings.html", current=current)
