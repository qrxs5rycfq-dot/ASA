"""Seed default data into the database."""

import hashlib

from app.extensions import get_db


def seed_all():
    """Seed all default data if tables are empty."""
    db = get_db()
    cursor = db.cursor()

    # Admin user
    cursor.execute("SELECT id FROM users LIMIT 1")
    if not cursor.fetchone():
        pw_hash = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            ("admin", pw_hash),
        )

    # Services
    cursor.execute("SELECT COUNT(*) AS c FROM services")
    if cursor.fetchone()["c"] == 0:
        for s in [
            ("bx-package", "General Supplier", "Penyediaan bahan dan peralatan industri berkualitas tinggi dengan harga kompetitif dan pengiriman tepat waktu ke seluruh Indonesia.", "from-red-500 to-rose-500", 1),
            ("bx-hard-hat", "Jasa Kontraktor", "Layanan konstruksi profesional untuk pembangunan infrastruktur, gedung, dan fasilitas industri dengan standar tinggi.", "from-blue-500 to-cyan-500", 2),
            ("bx-store-alt", "Pengadaan Material", "Supply chain management untuk material konstruksi dan peralatan industri dengan jaminan kualitas terbaik.", "from-purple-500 to-violet-500", 3),
            ("bx-search-alt", "Konsultasi Proyek", "Konsultasi teknis dan manajemen proyek oleh tenaga ahli berpengalaman di bidang konstruksi dan industri.", "from-green-500 to-emerald-500", 4),
            ("bx-wrench", "Perawatan & Renovasi", "Jasa pemeliharaan dan renovasi bangunan serta fasilitas untuk menjaga kualitas dan keamanan aset Anda.", "from-yellow-500 to-orange-500", 5),
            ("bx-line-chart", "Manajemen Konstruksi", "Pengelolaan proyek secara profesional dari perencanaan, pelaksanaan hingga serah terima kepada klien.", "from-pink-500 to-red-500", 6),
        ]:
            cursor.execute(
                "INSERT INTO services (icon, title, description, gradient, sort_order) VALUES (%s,%s,%s,%s,%s)", s
            )

    # Gallery
    cursor.execute("SELECT COUNT(*) AS c FROM gallery_items")
    if cursor.fetchone()["c"] == 0:
        for it in [
            ("Konstruksi Gedung Perkantoran", "PT. Nur Putra Mandiri", "Konstruksi", "bx-building", "from-red-600 to-green-600", 1),
            ("Pengadaan Peralatan Industri", "PT. Putra Syam Jaya", "Supply", "bx-cog", "from-violet-600 to-blue-600", 2),
            ("Pembangunan Infrastruktur Jalan", "CV. Asa Bangun Mandiri", "Infrastruktur", "bx-hard-hat", "from-yellow-500 to-red-600", 3),
            ("Renovasi Fasilitas Publik", "PT. Nur Putra Mandiri", "Renovasi", "bx-wrench", "from-green-500 to-emerald-500", 4),
            ("Supply Material Proyek Besar", "PT. Putra Syam Jaya", "Supply", "bx-package", "from-blue-500 to-cyan-500", 5),
            ("Pembangunan Gedung Komersial", "CV. Asa Bangun Mandiri", "Konstruksi", "bx-building-house", "from-orange-500 to-red-500", 6),
        ]:
            cursor.execute(
                "INSERT INTO gallery_items (title, company, category, icon, gradient, sort_order) VALUES (%s,%s,%s,%s,%s,%s)", it
            )

    # Testimonials
    cursor.execute("SELECT COUNT(*) AS c FROM testimonials")
    if cursor.fetchone()["c"] == 0:
        for t in [
            ("Ir. Ahmad Habibi", "Direktur Operasional", "PT. Mega Infrastruktur", "ASA Group selalu memberikan material berkualitas tinggi dengan pengiriman yang tepat waktu. Kami sangat puas dengan profesionalisme dan dedikasi tim mereka.", 5, "from-red-500 to-pink-500", 1),
            ("Drs. Bambang Setiawan", "Project Manager", "CV. Bina Karya Utama", "Kerjasama dengan PT. Putra Syam Jaya sangat memuaskan. Tim mereka memiliki pemahaman mendalam tentang kebutuhan industri dan selalu menawarkan solusi inovatif.", 5, "from-blue-500 to-cyan-500", 2),
            ("Hj. Siti Rahmawati", "Procurement Manager", "PT. Nusantara Jaya", "CV. Asa Bangun Mandiri telah menjadi mitra terpercaya kami. Kualitas pekerjaan konstruksi mereka sangat baik dan harga yang kompetitif.", 5, "from-yellow-500 to-orange-500", 3),
        ]:
            cursor.execute(
                "INSERT INTO testimonials (name, position, company, content, rating, avatar_gradient, sort_order) VALUES (%s,%s,%s,%s,%s,%s,%s)", t
            )

    # Clients
    cursor.execute("SELECT COUNT(*) AS c FROM clients")
    if cursor.fetchone()["c"] == 0:
        for c in [
            ("PT. Mega Infrastruktur", "bx-building", 1),
            ("CV. Bina Karya Utama", "bx-buildings", 2),
            ("PT. Nusantara Jaya", "bx-building-house", 3),
            ("PT. Maju Bersama", "bx-home-alt", 4),
            ("CV. Karya Mandiri", "bx-store", 5),
            ("PT. Sentosa Utama", "bx-cabinet", 6),
        ]:
            cursor.execute(
                "INSERT INTO clients (name, icon, sort_order) VALUES (%s,%s,%s)", c
            )

    # Team members
    cursor.execute("SELECT COUNT(*) AS c FROM team_members")
    if cursor.fetchone()["c"] == 0:
        for t in [
            ("H. Muhammad Syam", "Direktur Utama", "Pemimpin visioner ASA Group dengan pengalaman lebih dari 15 tahun di bidang supplier dan kontraktor.", "bx-user-circle", "from-purple-500 to-blue-500", 1),
            ("Ahmad Fauzi, ST", "Direktur Operasional", "Mengelola operasional harian dan memastikan kualitas layanan terjaga di semua lini perusahaan.", "bx-user-circle", "from-red-500 to-pink-500", 2),
            ("Ir. Nurul Hidayat", "Manajer Proyek", "Ahli manajemen proyek dengan sertifikasi profesional dalam bidang konstruksi dan infrastruktur.", "bx-user-circle", "from-green-500 to-emerald-500", 3),
            ("Sari Dewi, SE", "Manajer Keuangan", "Bertanggung jawab atas perencanaan keuangan dan pengelolaan anggaran seluruh entitas grup.", "bx-user-circle", "from-yellow-500 to-orange-500", 4),
        ]:
            cursor.execute(
                "INSERT INTO team_members (name, position, bio, icon, gradient, sort_order) VALUES (%s,%s,%s,%s,%s,%s)", t
            )

    # FAQs
    cursor.execute("SELECT COUNT(*) AS c FROM faqs")
    if cursor.fetchone()["c"] == 0:
        for f in [
            ("Apa saja layanan yang ditawarkan ASA Group?", "ASA Group menyediakan layanan General Supplier, Jasa Kontraktor, Pengadaan Material, Konsultasi Proyek, Perawatan & Renovasi, serta Manajemen Konstruksi.", 1),
            ("Bagaimana cara bermitra dengan ASA Group?", "Anda dapat menghubungi kami melalui halaman Kontak, WhatsApp, atau email. Tim kami akan merespons dan menjadwalkan konsultasi gratis.", 2),
            ("Apakah ASA Group melayani proyek di luar kota?", "Ya, kami melayani proyek di seluruh Indonesia. Tim profesional kami siap ditempatkan di berbagai lokasi proyek.", 3),
            ("Berapa lama proses pengadaan material?", "Waktu pengadaan bervariasi tergantung jenis dan jumlah material. Umumnya 3-14 hari kerja setelah PO disetujui.", 4),
            ("Apakah ada garansi untuk pekerjaan konstruksi?", "Ya, setiap proyek konstruksi kami dilengkapi garansi sesuai kesepakatan kontrak, umumnya 6-12 bulan setelah serah terima.", 5),
        ]:
            cursor.execute(
                "INSERT INTO faqs (question, answer, sort_order) VALUES (%s,%s,%s)", f
            )

    # Blog posts
    cursor.execute("SELECT COUNT(*) AS c FROM blog_posts")
    if cursor.fetchone()["c"] == 0:
        for p in [
            ("Tips Memilih Material Konstruksi Berkualitas", "tips-memilih-material-konstruksi", "Panduan lengkap memilih material konstruksi yang tepat untuk proyek Anda.", "Memilih material konstruksi yang berkualitas adalah langkah krusial dalam setiap proyek pembangunan.\n\n**1. Periksa Sertifikasi** — Pastikan material memiliki sertifikasi SNI.\n\n**2. Bandingkan Harga** — Jangan hanya tergiur harga murah.\n\n**3. Cek Reputasi Supplier** — Pilih supplier berpengalaman.\n\n**4. Perhatikan Garansi** — Material berkualitas dilengkapi garansi.\n\n**5. Konsultasi dengan Ahli** — Berkonsultasi dengan engineer untuk rekomendasi terbaik.", "bx-package", "from-red-500 to-orange-500", "Tips & Trik", "Admin"),
            ("Perkembangan Industri Konstruksi Indonesia 2024", "perkembangan-industri-konstruksi-2024", "Analisis tren dan perkembangan industri konstruksi di Indonesia.", "Industri konstruksi Indonesia terus menunjukkan pertumbuhan positif.\n\n**1. Digitalisasi Konstruksi** — Penggunaan BIM semakin meluas.\n\n**2. Green Building** — Kesadaran bangunan ramah lingkungan meningkat.\n\n**3. Infrastruktur Prioritas** — Pemerintah mendorong pembangunan infrastruktur strategis.\n\n**4. Material Inovatif** — Beton pracetak dan baja ringan semakin populer.", "bx-trending-up", "from-blue-500 to-cyan-500", "Industri", "Admin"),
            ("Pentingnya K3 dalam Proyek Konstruksi", "pentingnya-k3-proyek-konstruksi", "Memahami pentingnya Keselamatan dan Kesehatan Kerja dalam proyek konstruksi.", "K3 adalah aspek fundamental dalam setiap proyek konstruksi.\n\n**Mengapa K3 Penting?**\n- Melindungi nyawa dan kesehatan pekerja\n- Meningkatkan produktivitas kerja\n- Mengurangi biaya akibat kecelakaan\n- Memenuhi regulasi pemerintah\n\n**Implementasi K3 di ASA Group:**\n1. Pelatihan K3 rutin\n2. Penyediaan APD standar\n3. Inspeksi berkala\n4. Safety briefing harian\n5. Sistem pelaporan insiden transparan", "bx-shield-quarter", "from-green-500 to-emerald-500", "K3", "Admin"),
        ]:
            cursor.execute(
                "INSERT INTO blog_posts (title, slug, excerpt, content, cover_icon, cover_gradient, category, author) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", p
            )

    db.commit()
    cursor.close()
