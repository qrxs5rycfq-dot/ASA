import os
import hashlib
import secrets
from datetime import datetime
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    g,
)

import sqlite3

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))

DATABASE = os.path.join(app.instance_path, "asa.db")


def get_db():
    if "db" not in g:
        os.makedirs(app.instance_path, exist_ok=True)
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'admin'
    );
    CREATE TABLE IF NOT EXISTS blog_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        slug TEXT UNIQUE NOT NULL,
        excerpt TEXT,
        content TEXT NOT NULL,
        cover_icon TEXT DEFAULT 'bx-news',
        cover_gradient TEXT DEFAULT 'from-purple-600 to-blue-600',
        category TEXT DEFAULT 'Umum',
        author TEXT DEFAULT 'Admin',
        status TEXT DEFAULT 'published',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        icon TEXT DEFAULT 'bx-cog',
        title TEXT NOT NULL,
        description TEXT,
        gradient TEXT DEFAULT 'from-purple-500 to-blue-500',
        sort_order INTEGER DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS gallery_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT,
        category TEXT,
        icon TEXT DEFAULT 'bx-building',
        gradient TEXT DEFAULT 'from-purple-600 to-blue-600',
        sort_order INTEGER DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS testimonials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position TEXT,
        company TEXT,
        content TEXT NOT NULL,
        rating INTEGER DEFAULT 5,
        avatar_gradient TEXT DEFAULT 'from-purple-500 to-blue-500',
        sort_order INTEGER DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        icon TEXT DEFAULT 'bx-building',
        sort_order INTEGER DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS team_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position TEXT,
        bio TEXT,
        icon TEXT DEFAULT 'bx-user',
        gradient TEXT DEFAULT 'from-purple-500 to-blue-500',
        sort_order INTEGER DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS faqs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        sort_order INTEGER DEFAULT 0
    );
    """)

    # Seed default admin
    existing = db.execute("SELECT id FROM users LIMIT 1").fetchone()
    if not existing:
        pw_hash = hashlib.sha256("admin123".encode()).hexdigest()
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ("admin", pw_hash))

    # Seed services
    if db.execute("SELECT COUNT(*) as c FROM services").fetchone()["c"] == 0:
        for s in [
            ("bx-package", "General Supplier", "Penyediaan bahan dan peralatan industri berkualitas tinggi dengan harga kompetitif dan pengiriman tepat waktu ke seluruh Indonesia.", "from-red-500 to-rose-500", 1),
            ("bx-hard-hat", "Jasa Kontraktor", "Layanan konstruksi profesional untuk pembangunan infrastruktur, gedung, dan fasilitas industri dengan standar tinggi.", "from-blue-500 to-cyan-500", 2),
            ("bx-store-alt", "Pengadaan Material", "Supply chain management untuk material konstruksi dan peralatan industri dengan jaminan kualitas terbaik.", "from-purple-500 to-violet-500", 3),
            ("bx-search-alt", "Konsultasi Proyek", "Konsultasi teknis dan manajemen proyek oleh tenaga ahli berpengalaman di bidang konstruksi dan industri.", "from-green-500 to-emerald-500", 4),
            ("bx-wrench", "Perawatan & Renovasi", "Jasa pemeliharaan dan renovasi bangunan serta fasilitas untuk menjaga kualitas dan keamanan aset Anda.", "from-yellow-500 to-orange-500", 5),
            ("bx-line-chart", "Manajemen Konstruksi", "Pengelolaan proyek secara profesional dari perencanaan, pelaksanaan hingga serah terima kepada klien.", "from-pink-500 to-red-500", 6),
        ]:
            db.execute("INSERT INTO services (icon, title, description, gradient, sort_order) VALUES (?,?,?,?,?)", s)

    # Seed gallery
    if db.execute("SELECT COUNT(*) as c FROM gallery_items").fetchone()["c"] == 0:
        for it in [
            ("Konstruksi Gedung Perkantoran", "PT. Nur Putra Mandiri", "Konstruksi", "bx-building", "from-red-600 to-green-600", 1),
            ("Pengadaan Peralatan Industri", "PT. Putra Syam Jaya", "Supply", "bx-cog", "from-violet-600 to-blue-600", 2),
            ("Pembangunan Infrastruktur Jalan", "CV. Asa Bangun Mandiri", "Infrastruktur", "bx-hard-hat", "from-yellow-500 to-red-600", 3),
            ("Renovasi Fasilitas Publik", "PT. Nur Putra Mandiri", "Renovasi", "bx-wrench", "from-green-500 to-emerald-500", 4),
            ("Supply Material Proyek Besar", "PT. Putra Syam Jaya", "Supply", "bx-package", "from-blue-500 to-cyan-500", 5),
            ("Pembangunan Gedung Komersial", "CV. Asa Bangun Mandiri", "Konstruksi", "bx-building-house", "from-orange-500 to-red-500", 6),
        ]:
            db.execute("INSERT INTO gallery_items (title, company, category, icon, gradient, sort_order) VALUES (?,?,?,?,?,?)", it)

    # Seed testimonials
    if db.execute("SELECT COUNT(*) as c FROM testimonials").fetchone()["c"] == 0:
        for t in [
            ("Ir. Ahmad Habibi", "Direktur Operasional", "PT. Mega Infrastruktur", "ASA Group selalu memberikan material berkualitas tinggi dengan pengiriman yang tepat waktu. Kami sangat puas dengan profesionalisme dan dedikasi tim mereka.", 5, "from-red-500 to-pink-500", 1),
            ("Drs. Bambang Setiawan", "Project Manager", "CV. Bina Karya Utama", "Kerjasama dengan PT. Putra Syam Jaya sangat memuaskan. Tim mereka memiliki pemahaman mendalam tentang kebutuhan industri dan selalu menawarkan solusi inovatif.", 5, "from-blue-500 to-cyan-500", 2),
            ("Hj. Siti Rahmawati", "Procurement Manager", "PT. Nusantara Jaya", "CV. Asa Bangun Mandiri telah menjadi mitra terpercaya kami. Kualitas pekerjaan konstruksi mereka sangat baik dan harga yang kompetitif.", 5, "from-yellow-500 to-orange-500", 3),
        ]:
            db.execute("INSERT INTO testimonials (name, position, company, content, rating, avatar_gradient, sort_order) VALUES (?,?,?,?,?,?,?)", t)

    # Seed clients
    if db.execute("SELECT COUNT(*) as c FROM clients").fetchone()["c"] == 0:
        for c in [("PT. Mega Infrastruktur","bx-building",1),("CV. Bina Karya Utama","bx-buildings",2),("PT. Nusantara Jaya","bx-building-house",3),("PT. Maju Bersama","bx-home-alt",4),("CV. Karya Mandiri","bx-store",5),("PT. Sentosa Utama","bx-cabinet",6)]:
            db.execute("INSERT INTO clients (name, icon, sort_order) VALUES (?,?,?)", c)

    # Seed team
    if db.execute("SELECT COUNT(*) as c FROM team_members").fetchone()["c"] == 0:
        for t in [
            ("H. Muhammad Syam", "Direktur Utama", "Pemimpin visioner ASA Group dengan pengalaman lebih dari 15 tahun di bidang supplier dan kontraktor.", "bx-user-circle", "from-purple-500 to-blue-500", 1),
            ("Ahmad Fauzi, ST", "Direktur Operasional", "Mengelola operasional harian dan memastikan kualitas layanan terjaga di semua lini perusahaan.", "bx-user-circle", "from-red-500 to-pink-500", 2),
            ("Ir. Nurul Hidayat", "Manajer Proyek", "Ahli manajemen proyek dengan sertifikasi profesional dalam bidang konstruksi dan infrastruktur.", "bx-user-circle", "from-green-500 to-emerald-500", 3),
            ("Sari Dewi, SE", "Manajer Keuangan", "Bertanggung jawab atas perencanaan keuangan dan pengelolaan anggaran seluruh entitas grup.", "bx-user-circle", "from-yellow-500 to-orange-500", 4),
        ]:
            db.execute("INSERT INTO team_members (name, position, bio, icon, gradient, sort_order) VALUES (?,?,?,?,?,?)", t)

    # Seed FAQs
    if db.execute("SELECT COUNT(*) as c FROM faqs").fetchone()["c"] == 0:
        for f in [
            ("Apa saja layanan yang ditawarkan ASA Group?", "ASA Group menyediakan layanan General Supplier, Jasa Kontraktor, Pengadaan Material, Konsultasi Proyek, Perawatan & Renovasi, serta Manajemen Konstruksi.", 1),
            ("Bagaimana cara bermitra dengan ASA Group?", "Anda dapat menghubungi kami melalui halaman Kontak, WhatsApp, atau email. Tim kami akan merespons dan menjadwalkan konsultasi gratis.", 2),
            ("Apakah ASA Group melayani proyek di luar kota?", "Ya, kami melayani proyek di seluruh Indonesia. Tim profesional kami siap ditempatkan di berbagai lokasi proyek.", 3),
            ("Berapa lama proses pengadaan material?", "Waktu pengadaan bervariasi tergantung jenis dan jumlah material. Umumnya 3-14 hari kerja setelah PO disetujui.", 4),
            ("Apakah ada garansi untuk pekerjaan konstruksi?", "Ya, setiap proyek konstruksi kami dilengkapi garansi sesuai kesepakatan kontrak, umumnya 6-12 bulan setelah serah terima.", 5),
        ]:
            db.execute("INSERT INTO faqs (question, answer, sort_order) VALUES (?,?,?)", f)

    # Seed blog posts
    if db.execute("SELECT COUNT(*) as c FROM blog_posts").fetchone()["c"] == 0:
        for p in [
            ("Tips Memilih Material Konstruksi Berkualitas", "tips-memilih-material-konstruksi", "Panduan lengkap memilih material konstruksi yang tepat untuk proyek Anda.", "Memilih material konstruksi yang berkualitas adalah langkah krusial dalam setiap proyek pembangunan.\n\n**1. Periksa Sertifikasi** — Pastikan material memiliki sertifikasi SNI.\n\n**2. Bandingkan Harga** — Jangan hanya tergiur harga murah.\n\n**3. Cek Reputasi Supplier** — Pilih supplier berpengalaman.\n\n**4. Perhatikan Garansi** — Material berkualitas dilengkapi garansi.\n\n**5. Konsultasi dengan Ahli** — Berkonsultasi dengan engineer untuk rekomendasi terbaik.", "bx-package", "from-red-500 to-orange-500", "Tips & Trik", "Admin"),
            ("Perkembangan Industri Konstruksi Indonesia 2024", "perkembangan-industri-konstruksi-2024", "Analisis tren dan perkembangan industri konstruksi di Indonesia.", "Industri konstruksi Indonesia terus menunjukkan pertumbuhan positif.\n\n**1. Digitalisasi Konstruksi** — Penggunaan BIM semakin meluas.\n\n**2. Green Building** — Kesadaran bangunan ramah lingkungan meningkat.\n\n**3. Infrastruktur Prioritas** — Pemerintah mendorong pembangunan infrastruktur strategis.\n\n**4. Material Inovatif** — Beton pracetak dan baja ringan semakin populer.", "bx-trending-up", "from-blue-500 to-cyan-500", "Industri", "Admin"),
            ("Pentingnya K3 dalam Proyek Konstruksi", "pentingnya-k3-proyek-konstruksi", "Memahami pentingnya Keselamatan dan Kesehatan Kerja dalam proyek konstruksi.", "K3 adalah aspek fundamental dalam setiap proyek konstruksi.\n\n**Mengapa K3 Penting?**\n- Melindungi nyawa dan kesehatan pekerja\n- Meningkatkan produktivitas kerja\n- Mengurangi biaya akibat kecelakaan\n- Memenuhi regulasi pemerintah\n\n**Implementasi K3 di ASA Group:**\n1. Pelatihan K3 rutin\n2. Penyediaan APD standar\n3. Inspeksi berkala\n4. Safety briefing harian\n5. Sistem pelaporan insiden transparan", "bx-shield-quarter", "from-green-500 to-emerald-500", "K3", "Admin"),
        ]:
            db.execute("INSERT INTO blog_posts (title, slug, excerpt, content, cover_icon, cover_gradient, category, author) VALUES (?,?,?,?,?,?,?,?)", p)

    db.commit()


COMPANIES = {
    "nur-putra-mandiri": {
        "name": "PT. Nur Putra Mandiri",
        "slug": "nur-putra-mandiri",
        "tagline": "Keunggulan dalam Setiap Solusi",
        "colors": {
            "primary": "#DC2626", "secondary": "#16A34A", "tertiary": "#111827",
            "gradient": "from-red-600 via-gray-900 to-green-600",
            "gradient_short": "from-red-600 to-green-600",
            "bg": "bg-red-600", "bg_secondary": "bg-green-600",
            "text": "text-red-600", "text_secondary": "text-green-600",
            "border": "border-red-600", "ring": "ring-red-600",
        },
        "description": "PT. Nur Putra Mandiri merupakan perusahaan swasta yang bergerak dalam bidang perdagangan umum dan jasa sebagai General Supplier & Kontraktor. Kami selalu menekankan pada aspek profesionalitas, berorientasi pada kualitas dan ketepatan waktu dalam melayani kebutuhan pelanggan.",
        "founded": "2018",
        "specialties": ["Pengadaan Material Konstruksi", "Supplier Peralatan Industri", "Jasa Konstruksi Bangunan", "Renovasi & Pemeliharaan"],
        "icon": "bx-buildings",
    },
    "putra-syam-jaya": {
        "name": "PT. Putra Syam Jaya",
        "slug": "putra-syam-jaya",
        "tagline": "Inovasi Tanpa Batas",
        "colors": {
            "primary": "#7C3AED", "secondary": "#2563EB", "tertiary": "#1e1b4b",
            "gradient": "from-violet-600 to-blue-600",
            "gradient_short": "from-violet-600 to-blue-600",
            "bg": "bg-violet-600", "bg_secondary": "bg-blue-600",
            "text": "text-violet-600", "text_secondary": "text-blue-600",
            "border": "border-violet-600", "ring": "ring-violet-600",
        },
        "description": "PT. Putra Syam Jaya merupakan perusahaan swasta yang bergerak dalam bidang perdagangan umum dan jasa sebagai General Supplier & Kontraktor. Kami menjadi mitra terpercaya dalam pengadaan bahan dan peralatan industri dengan standar kualitas internasional.",
        "founded": "2019",
        "specialties": ["Supplier Peralatan Berat", "Pengadaan Bahan Bangunan", "Konsultasi Proyek", "Manajemen Konstruksi"],
        "icon": "bx-cube-alt",
    },
    "asa-bangun-mandiri": {
        "name": "CV. Asa Bangun Mandiri",
        "slug": "asa-bangun-mandiri",
        "tagline": "Membangun Masa Depan",
        "colors": {
            "primary": "#F59E0B", "secondary": "#DC2626", "tertiary": "#78350f",
            "gradient": "from-yellow-500 to-red-600",
            "gradient_short": "from-yellow-500 to-red-600",
            "bg": "bg-yellow-500", "bg_secondary": "bg-red-600",
            "text": "text-yellow-500", "text_secondary": "text-red-600",
            "border": "border-yellow-500", "ring": "ring-yellow-500",
        },
        "description": "CV. Asa Bangun Mandiri merupakan perusahaan swasta yang bergerak dalam bidang perdagangan umum dan jasa sebagai General Supplier & Kontraktor. Kami hadir sebagai kontraktor handal dengan dedikasi tinggi dalam pembangunan infrastruktur dan proyek konstruksi.",
        "founded": "2020",
        "specialties": ["Konstruksi Infrastruktur", "Pembangunan Gedung", "Supplier Material Premium", "Jasa Perawatan Fasilitas"],
        "icon": "bx-hard-hat",
    },
}

COMPANY_LIST = [
    {"name": "PT. Nur Putra Mandiri", "slug": "nur-putra-mandiri", "tagline": "Keunggulan dalam Setiap Solusi", "colors": {"primary": "#DC2626", "secondary": "#16A34A", "gradient": "from-red-600 to-green-600"}, "description": "Perusahaan yang bergerak dalam bidang perdagangan umum dan jasa, mengutamakan profesionalitas dan kualitas tinggi.", "icon": "bx-buildings"},
    {"name": "PT. Putra Syam Jaya", "slug": "putra-syam-jaya", "tagline": "Inovasi Tanpa Batas", "colors": {"primary": "#7C3AED", "secondary": "#2563EB", "gradient": "from-violet-600 to-blue-600"}, "description": "Mitra terpercaya dalam pengadaan bahan dan peralatan industri dengan standar kualitas internasional.", "icon": "bx-cube-alt"},
    {"name": "CV. Asa Bangun Mandiri", "slug": "asa-bangun-mandiri", "tagline": "Membangun Masa Depan", "colors": {"primary": "#F59E0B", "secondary": "#DC2626", "gradient": "from-yellow-500 to-red-600"}, "description": "Kontraktor handal dengan dedikasi tinggi dalam pembangunan infrastruktur dan proyek konstruksi.", "icon": "bx-hard-hat"},
]


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Silakan login terlebih dahulu.", "warning")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


@app.before_request
def before_request():
    if not getattr(app, '_db_initialized', False):
        init_db()
        app._db_initialized = True


# ---- PUBLIC ROUTES ----

@app.route("/")
def index():
    db = get_db()
    services = db.execute("SELECT * FROM services ORDER BY sort_order").fetchall()
    testimonials = db.execute("SELECT * FROM testimonials ORDER BY sort_order").fetchall()
    clients = db.execute("SELECT * FROM clients ORDER BY sort_order").fetchall()
    latest_posts = db.execute("SELECT * FROM blog_posts WHERE status='published' ORDER BY created_at DESC LIMIT 3").fetchall()
    return render_template("index.html", companies=COMPANY_LIST, services=services, testimonials=testimonials, clients=clients, latest_posts=latest_posts)


@app.route("/about")
def about():
    db = get_db()
    team = db.execute("SELECT * FROM team_members ORDER BY sort_order").fetchall()
    faqs = db.execute("SELECT * FROM faqs ORDER BY sort_order").fetchall()
    return render_template("about.html", team=team, faqs=faqs)


@app.route("/services")
def services_page():
    db = get_db()
    services = db.execute("SELECT * FROM services ORDER BY sort_order").fetchall()
    return render_template("services.html", services=services)


@app.route("/gallery")
def gallery_page():
    db = get_db()
    gallery = db.execute("SELECT * FROM gallery_items ORDER BY sort_order").fetchall()
    return render_template("gallery.html", gallery=gallery)


@app.route("/company/<slug>")
def company(slug):
    company_data = COMPANIES.get(slug)
    if not company_data:
        return render_template("404.html"), 404
    return render_template("company.html", company=company_data)


@app.route("/blog")
def blog_list():
    db = get_db()
    page = request.args.get("page", 1, type=int)
    per_page = 6
    offset = (page - 1) * per_page
    total = db.execute("SELECT COUNT(*) as c FROM blog_posts WHERE status='published'").fetchone()["c"]
    posts = db.execute("SELECT * FROM blog_posts WHERE status='published' ORDER BY created_at DESC LIMIT ? OFFSET ?", (per_page, offset)).fetchall()
    total_pages = max(1, (total + per_page - 1) // per_page)
    return render_template("blog.html", posts=posts, page=page, total_pages=total_pages)


@app.route("/blog/<slug>")
def blog_detail(slug):
    db = get_db()
    post = db.execute("SELECT * FROM blog_posts WHERE slug=? AND status='published'", (slug,)).fetchone()
    if not post:
        return render_template("404.html"), 404
    recent = db.execute("SELECT * FROM blog_posts WHERE status='published' AND slug!=? ORDER BY created_at DESC LIMIT 3", (slug,)).fetchall()
    return render_template("blog_detail.html", post=post, recent_posts=recent)


@app.route("/contact")
def contact_page():
    return render_template("contact.html")


# ---- ADMIN ROUTES ----

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        pw_hash = hashlib.sha256(password.encode()).hexdigest()
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username=? AND password_hash=?", (username, pw_hash)).fetchone()
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Login berhasil!", "success")
            return redirect(url_for("admin_dashboard"))
        flash("Username atau password salah.", "error")
    return render_template("admin/login.html")


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    flash("Logout berhasil.", "success")
    return redirect(url_for("admin_login"))


@app.route("/admin")
@login_required
def admin_dashboard():
    db = get_db()
    stats = {
        "posts": db.execute("SELECT COUNT(*) as c FROM blog_posts").fetchone()["c"],
        "services": db.execute("SELECT COUNT(*) as c FROM services").fetchone()["c"],
        "gallery": db.execute("SELECT COUNT(*) as c FROM gallery_items").fetchone()["c"],
        "testimonials": db.execute("SELECT COUNT(*) as c FROM testimonials").fetchone()["c"],
        "clients": db.execute("SELECT COUNT(*) as c FROM clients").fetchone()["c"],
        "team": db.execute("SELECT COUNT(*) as c FROM team_members").fetchone()["c"],
        "faqs": db.execute("SELECT COUNT(*) as c FROM faqs").fetchone()["c"],
    }
    recent_posts = db.execute("SELECT * FROM blog_posts ORDER BY created_at DESC LIMIT 5").fetchall()
    return render_template("admin/dashboard.html", stats=stats, recent_posts=recent_posts)


# Blog CRUD
@app.route("/admin/blog")
@login_required
def admin_blog_list():
    db = get_db()
    posts = db.execute("SELECT * FROM blog_posts ORDER BY created_at DESC").fetchall()
    return render_template("admin/blog_list.html", posts=posts)


@app.route("/admin/blog/create", methods=["GET", "POST"])
@login_required
def admin_blog_create():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        slug = request.form.get("slug", "").strip() or title.lower().replace(" ", "-")
        slug = "".join(c if c.isalnum() or c == "-" else "-" for c in slug).strip("-")
        excerpt = request.form.get("excerpt", "").strip()
        content = request.form.get("content", "").strip()
        category = request.form.get("category", "Umum").strip()
        cover_icon = request.form.get("cover_icon", "bx-news").strip()
        cover_gradient = request.form.get("cover_gradient", "from-purple-600 to-blue-600").strip()
        status = request.form.get("status", "published")
        author = session.get("username", "Admin")
        db = get_db()
        try:
            db.execute("INSERT INTO blog_posts (title, slug, excerpt, content, cover_icon, cover_gradient, category, author, status) VALUES (?,?,?,?,?,?,?,?,?)",
                       (title, slug, excerpt, content, cover_icon, cover_gradient, category, author, status))
            db.commit()
            flash("Blog post berhasil dibuat!", "success")
            return redirect(url_for("admin_blog_list"))
        except sqlite3.IntegrityError:
            flash("Slug sudah digunakan.", "error")
    return render_template("admin/blog_form.html", post=None)


@app.route("/admin/blog/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def admin_blog_edit(post_id):
    db = get_db()
    post = db.execute("SELECT * FROM blog_posts WHERE id=?", (post_id,)).fetchone()
    if not post:
        flash("Post tidak ditemukan.", "error")
        return redirect(url_for("admin_blog_list"))
    if request.method == "POST":
        try:
            db.execute("UPDATE blog_posts SET title=?, slug=?, excerpt=?, content=?, cover_icon=?, cover_gradient=?, category=?, status=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
                       (request.form["title"].strip(), request.form["slug"].strip(), request.form.get("excerpt","").strip(), request.form["content"].strip(),
                        request.form.get("cover_icon","bx-news").strip(), request.form.get("cover_gradient","from-purple-600 to-blue-600").strip(),
                        request.form.get("category","Umum").strip(), request.form.get("status","published"), post_id))
            db.commit()
            flash("Blog post berhasil diperbarui!", "success")
            return redirect(url_for("admin_blog_list"))
        except sqlite3.IntegrityError:
            flash("Slug sudah digunakan.", "error")
    return render_template("admin/blog_form.html", post=post)


@app.route("/admin/blog/<int:post_id>/delete", methods=["POST"])
@login_required
def admin_blog_delete(post_id):
    db = get_db()
    db.execute("DELETE FROM blog_posts WHERE id=?", (post_id,))
    db.commit()
    flash("Blog post berhasil dihapus.", "success")
    return redirect(url_for("admin_blog_list"))


# Services CRUD
@app.route("/admin/services")
@login_required
def admin_services_list():
    db = get_db()
    services = db.execute("SELECT * FROM services ORDER BY sort_order").fetchall()
    return render_template("admin/services_list.html", services=services)


@app.route("/admin/services/create", methods=["GET", "POST"])
@login_required
def admin_service_create():
    if request.method == "POST":
        db = get_db()
        db.execute("INSERT INTO services (icon, title, description, gradient, sort_order) VALUES (?,?,?,?,?)",
                   (request.form["icon"], request.form["title"], request.form["description"], request.form["gradient"], request.form.get("sort_order", 0, type=int)))
        db.commit()
        flash("Layanan berhasil ditambahkan!", "success")
        return redirect(url_for("admin_services_list"))
    return render_template("admin/service_form.html", service=None)


@app.route("/admin/services/<int:sid>/edit", methods=["GET", "POST"])
@login_required
def admin_service_edit(sid):
    db = get_db()
    service = db.execute("SELECT * FROM services WHERE id=?", (sid,)).fetchone()
    if not service:
        flash("Layanan tidak ditemukan.", "error")
        return redirect(url_for("admin_services_list"))
    if request.method == "POST":
        db.execute("UPDATE services SET icon=?, title=?, description=?, gradient=?, sort_order=? WHERE id=?",
                   (request.form["icon"], request.form["title"], request.form["description"], request.form["gradient"], request.form.get("sort_order", 0, type=int), sid))
        db.commit()
        flash("Layanan berhasil diperbarui!", "success")
        return redirect(url_for("admin_services_list"))
    return render_template("admin/service_form.html", service=service)


@app.route("/admin/services/<int:sid>/delete", methods=["POST"])
@login_required
def admin_service_delete(sid):
    db = get_db()
    db.execute("DELETE FROM services WHERE id=?", (sid,))
    db.commit()
    flash("Layanan berhasil dihapus.", "success")
    return redirect(url_for("admin_services_list"))


# Testimonials CRUD
@app.route("/admin/testimonials")
@login_required
def admin_testimonials():
    db = get_db()
    items = db.execute("SELECT * FROM testimonials ORDER BY sort_order").fetchall()
    return render_template("admin/testimonials_list.html", items=items)


@app.route("/admin/testimonials/create", methods=["GET", "POST"])
@login_required
def admin_testimonial_create():
    if request.method == "POST":
        db = get_db()
        db.execute("INSERT INTO testimonials (name, position, company, content, rating, avatar_gradient, sort_order) VALUES (?,?,?,?,?,?,?)",
                   (request.form["name"], request.form["position"], request.form["company"], request.form["content"],
                    request.form.get("rating", 5, type=int), request.form.get("avatar_gradient", "from-purple-500 to-blue-500"), request.form.get("sort_order", 0, type=int)))
        db.commit()
        flash("Testimoni berhasil ditambahkan!", "success")
        return redirect(url_for("admin_testimonials"))
    return render_template("admin/testimonial_form.html", item=None)


@app.route("/admin/testimonials/<int:tid>/edit", methods=["GET", "POST"])
@login_required
def admin_testimonial_edit(tid):
    db = get_db()
    item = db.execute("SELECT * FROM testimonials WHERE id=?", (tid,)).fetchone()
    if not item:
        flash("Testimoni tidak ditemukan.", "error")
        return redirect(url_for("admin_testimonials"))
    if request.method == "POST":
        db.execute("UPDATE testimonials SET name=?, position=?, company=?, content=?, rating=?, avatar_gradient=?, sort_order=? WHERE id=?",
                   (request.form["name"], request.form["position"], request.form["company"], request.form["content"],
                    request.form.get("rating", 5, type=int), request.form.get("avatar_gradient", "from-purple-500 to-blue-500"), request.form.get("sort_order", 0, type=int), tid))
        db.commit()
        flash("Testimoni berhasil diperbarui!", "success")
        return redirect(url_for("admin_testimonials"))
    return render_template("admin/testimonial_form.html", item=item)


@app.route("/admin/testimonials/<int:tid>/delete", methods=["POST"])
@login_required
def admin_testimonial_delete(tid):
    db = get_db()
    db.execute("DELETE FROM testimonials WHERE id=?", (tid,))
    db.commit()
    flash("Testimoni berhasil dihapus.", "success")
    return redirect(url_for("admin_testimonials"))


# Gallery CRUD
@app.route("/admin/gallery")
@login_required
def admin_gallery():
    db = get_db()
    items = db.execute("SELECT * FROM gallery_items ORDER BY sort_order").fetchall()
    return render_template("admin/gallery_list.html", items=items)


@app.route("/admin/gallery/create", methods=["GET", "POST"])
@login_required
def admin_gallery_create():
    if request.method == "POST":
        db = get_db()
        db.execute("INSERT INTO gallery_items (title, company, category, icon, gradient, sort_order) VALUES (?,?,?,?,?,?)",
                   (request.form["title"], request.form["company"], request.form["category"], request.form.get("icon","bx-building"), request.form.get("gradient","from-purple-600 to-blue-600"), request.form.get("sort_order",0,type=int)))
        db.commit()
        flash("Item galeri berhasil ditambahkan!", "success")
        return redirect(url_for("admin_gallery"))
    return render_template("admin/gallery_form.html", item=None)


@app.route("/admin/gallery/<int:gid>/edit", methods=["GET", "POST"])
@login_required
def admin_gallery_edit(gid):
    db = get_db()
    item = db.execute("SELECT * FROM gallery_items WHERE id=?", (gid,)).fetchone()
    if not item:
        flash("Item tidak ditemukan.", "error")
        return redirect(url_for("admin_gallery"))
    if request.method == "POST":
        db.execute("UPDATE gallery_items SET title=?, company=?, category=?, icon=?, gradient=?, sort_order=? WHERE id=?",
                   (request.form["title"], request.form["company"], request.form["category"], request.form.get("icon","bx-building"), request.form.get("gradient","from-purple-600 to-blue-600"), request.form.get("sort_order",0,type=int), gid))
        db.commit()
        flash("Item galeri berhasil diperbarui!", "success")
        return redirect(url_for("admin_gallery"))
    return render_template("admin/gallery_form.html", item=item)


@app.route("/admin/gallery/<int:gid>/delete", methods=["POST"])
@login_required
def admin_gallery_delete(gid):
    db = get_db()
    db.execute("DELETE FROM gallery_items WHERE id=?", (gid,))
    db.commit()
    flash("Item galeri berhasil dihapus.", "success")
    return redirect(url_for("admin_gallery"))


# Team CRUD
@app.route("/admin/team")
@login_required
def admin_team():
    db = get_db()
    items = db.execute("SELECT * FROM team_members ORDER BY sort_order").fetchall()
    return render_template("admin/team_list.html", items=items)


@app.route("/admin/team/create", methods=["GET", "POST"])
@login_required
def admin_team_create():
    if request.method == "POST":
        db = get_db()
        db.execute("INSERT INTO team_members (name, position, bio, icon, gradient, sort_order) VALUES (?,?,?,?,?,?)",
                   (request.form["name"], request.form["position"], request.form["bio"], request.form.get("icon","bx-user-circle"), request.form.get("gradient","from-purple-500 to-blue-500"), request.form.get("sort_order",0,type=int)))
        db.commit()
        flash("Anggota tim berhasil ditambahkan!", "success")
        return redirect(url_for("admin_team"))
    return render_template("admin/team_form.html", item=None)


@app.route("/admin/team/<int:tid>/edit", methods=["GET", "POST"])
@login_required
def admin_team_edit(tid):
    db = get_db()
    item = db.execute("SELECT * FROM team_members WHERE id=?", (tid,)).fetchone()
    if not item:
        flash("Anggota tim tidak ditemukan.", "error")
        return redirect(url_for("admin_team"))
    if request.method == "POST":
        db.execute("UPDATE team_members SET name=?, position=?, bio=?, icon=?, gradient=?, sort_order=? WHERE id=?",
                   (request.form["name"], request.form["position"], request.form["bio"], request.form.get("icon","bx-user-circle"), request.form.get("gradient","from-purple-500 to-blue-500"), request.form.get("sort_order",0,type=int), tid))
        db.commit()
        flash("Anggota tim berhasil diperbarui!", "success")
        return redirect(url_for("admin_team"))
    return render_template("admin/team_form.html", item=item)


@app.route("/admin/team/<int:tid>/delete", methods=["POST"])
@login_required
def admin_team_delete(tid):
    db = get_db()
    db.execute("DELETE FROM team_members WHERE id=?", (tid,))
    db.commit()
    flash("Anggota tim berhasil dihapus.", "success")
    return redirect(url_for("admin_team"))


# FAQ CRUD
@app.route("/admin/faqs")
@login_required
def admin_faqs():
    db = get_db()
    items = db.execute("SELECT * FROM faqs ORDER BY sort_order").fetchall()
    return render_template("admin/faq_list.html", items=items)


@app.route("/admin/faqs/create", methods=["GET", "POST"])
@login_required
def admin_faq_create():
    if request.method == "POST":
        db = get_db()
        db.execute("INSERT INTO faqs (question, answer, sort_order) VALUES (?,?,?)",
                   (request.form["question"], request.form["answer"], request.form.get("sort_order",0,type=int)))
        db.commit()
        flash("FAQ berhasil ditambahkan!", "success")
        return redirect(url_for("admin_faqs"))
    return render_template("admin/faq_form.html", item=None)


@app.route("/admin/faqs/<int:fid>/edit", methods=["GET", "POST"])
@login_required
def admin_faq_edit(fid):
    db = get_db()
    item = db.execute("SELECT * FROM faqs WHERE id=?", (fid,)).fetchone()
    if not item:
        flash("FAQ tidak ditemukan.", "error")
        return redirect(url_for("admin_faqs"))
    if request.method == "POST":
        db.execute("UPDATE faqs SET question=?, answer=?, sort_order=? WHERE id=?",
                   (request.form["question"], request.form["answer"], request.form.get("sort_order",0,type=int), fid))
        db.commit()
        flash("FAQ berhasil diperbarui!", "success")
        return redirect(url_for("admin_faqs"))
    return render_template("admin/faq_form.html", item=item)


@app.route("/admin/faqs/<int:fid>/delete", methods=["POST"])
@login_required
def admin_faq_delete(fid):
    db = get_db()
    db.execute("DELETE FROM faqs WHERE id=?", (fid,))
    db.commit()
    flash("FAQ berhasil dihapus.", "success")
    return redirect(url_for("admin_faqs"))


# Clients CRUD
@app.route("/admin/clients")
@login_required
def admin_clients():
    db = get_db()
    items = db.execute("SELECT * FROM clients ORDER BY sort_order").fetchall()
    return render_template("admin/client_list.html", items=items)


@app.route("/admin/clients/create", methods=["GET", "POST"])
@login_required
def admin_client_create():
    if request.method == "POST":
        db = get_db()
        db.execute("INSERT INTO clients (name, icon, sort_order) VALUES (?,?,?)",
                   (request.form["name"], request.form.get("icon","bx-building"), request.form.get("sort_order",0,type=int)))
        db.commit()
        flash("Klien berhasil ditambahkan!", "success")
        return redirect(url_for("admin_clients"))
    return render_template("admin/client_form.html", item=None)


@app.route("/admin/clients/<int:cid>/edit", methods=["GET", "POST"])
@login_required
def admin_client_edit(cid):
    db = get_db()
    item = db.execute("SELECT * FROM clients WHERE id=?", (cid,)).fetchone()
    if not item:
        flash("Klien tidak ditemukan.", "error")
        return redirect(url_for("admin_clients"))
    if request.method == "POST":
        db.execute("UPDATE clients SET name=?, icon=?, sort_order=? WHERE id=?",
                   (request.form["name"], request.form.get("icon","bx-building"), request.form.get("sort_order",0,type=int), cid))
        db.commit()
        flash("Klien berhasil diperbarui!", "success")
        return redirect(url_for("admin_clients"))
    return render_template("admin/client_form.html", item=item)


@app.route("/admin/clients/<int:cid>/delete", methods=["POST"])
@login_required
def admin_client_delete(cid):
    db = get_db()
    db.execute("DELETE FROM clients WHERE id=?", (cid,))
    db.commit()
    flash("Klien berhasil dihapus.", "success")
    return redirect(url_for("admin_clients"))


# Change password
@app.route("/admin/change-password", methods=["GET", "POST"])
@login_required
def admin_change_password():
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
            current_hash = hashlib.sha256(current.encode()).hexdigest()
            user = db.execute("SELECT * FROM users WHERE id=? AND password_hash=?", (session["user_id"], current_hash)).fetchone()
            if not user:
                flash("Password lama salah.", "error")
            else:
                new_hash = hashlib.sha256(new_pw.encode()).hexdigest()
                db.execute("UPDATE users SET password_hash=? WHERE id=?", (new_hash, session["user_id"]))
                db.commit()
                flash("Password berhasil diubah!", "success")
                return redirect(url_for("admin_dashboard"))
    return render_template("admin/change_password.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
