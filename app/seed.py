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

    # Site settings
    cursor.execute("SELECT COUNT(*) AS c FROM site_settings")
    if cursor.fetchone()["c"] == 0:
        for k, v in [
            ("app_name", "ASA Group"),
            ("logo_url", ""),
            ("tagline", "General Supplier & Kontraktor"),
        ]:
            cursor.execute(
                "INSERT INTO site_settings (setting_key, setting_value) VALUES (%s, %s)",
                (k, v),
            )

    # Services
    cursor.execute("SELECT COUNT(*) AS c FROM services")
    if cursor.fetchone()["c"] == 0:
        for s in [
            ("bx-package", "General Supplier", "Penyediaan bahan dan peralatan industri berkualitas tinggi dengan harga kompetitif dan pengiriman tepat waktu ke seluruh Indonesia.", "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=600&q=80", "from-red-500 to-rose-500", 1),
            ("bx-hard-hat", "Jasa Kontraktor", "Layanan konstruksi profesional untuk pembangunan infrastruktur, gedung, dan fasilitas industri dengan standar tinggi.", "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=600&q=80", "from-blue-500 to-cyan-500", 2),
            ("bx-store-alt", "Pengadaan Material", "Supply chain management untuk material konstruksi dan peralatan industri dengan jaminan kualitas terbaik.", "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=600&q=80", "from-purple-500 to-violet-500", 3),
            ("bx-search-alt", "Konsultasi Proyek", "Konsultasi teknis dan manajemen proyek oleh tenaga ahli berpengalaman di bidang konstruksi dan industri.", "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=600&q=80", "from-green-500 to-emerald-500", 4),
            ("bx-wrench", "Perawatan & Renovasi", "Jasa pemeliharaan dan renovasi bangunan serta fasilitas untuk menjaga kualitas dan keamanan aset Anda.", "https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=600&q=80", "from-yellow-500 to-orange-500", 5),
            ("bx-line-chart", "Manajemen Konstruksi", "Pengelolaan proyek secara profesional dari perencanaan, pelaksanaan hingga serah terima kepada klien.", "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=600&q=80", "from-pink-500 to-red-500", 6),
        ]:
            cursor.execute(
                "INSERT INTO services (icon, title, description, image_url, gradient, sort_order) VALUES (%s,%s,%s,%s,%s,%s)", s
            )

    # Gallery
    cursor.execute("SELECT COUNT(*) AS c FROM gallery_items")
    if cursor.fetchone()["c"] == 0:
        for it in [
            ("Konstruksi Gedung Perkantoran", "PT. Nur Putra Mandiri", "Konstruksi", "https://images.unsplash.com/photo-1486325212027-8081e485255e?w=600&q=80", "bx-building", "from-red-600 to-green-600", 1),
            ("Pengadaan Peralatan Industri", "PT. Putra Syam Jaya", "Supply", "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=600&q=80", "bx-cog", "from-violet-600 to-blue-600", 2),
            ("Pembangunan Infrastruktur Jalan", "CV. Asa Bangun Mandiri", "Infrastruktur", "https://images.unsplash.com/photo-1545558014-8692077e9b5c?w=600&q=80", "bx-hard-hat", "from-yellow-500 to-red-600", 3),
            ("Renovasi Fasilitas Publik", "PT. Nur Putra Mandiri", "Renovasi", "https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=600&q=80", "bx-wrench", "from-green-500 to-emerald-500", 4),
            ("Supply Material Proyek Besar", "PT. Putra Syam Jaya", "Supply", "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=600&q=80", "bx-package", "from-blue-500 to-cyan-500", 5),
            ("Pembangunan Gedung Komersial", "CV. Asa Bangun Mandiri", "Konstruksi", "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=600&q=80", "bx-building-house", "from-orange-500 to-red-500", 6),
        ]:
            cursor.execute(
                "INSERT INTO gallery_items (title, company, category, image_url, icon, gradient, sort_order) VALUES (%s,%s,%s,%s,%s,%s,%s)", it
            )

    # Testimonials
    cursor.execute("SELECT COUNT(*) AS c FROM testimonials")
    if cursor.fetchone()["c"] == 0:
        for t in [
            ("Ir. Ahmad Habibi", "Direktur Operasional", "PT. Mega Infrastruktur", "ASA Group selalu memberikan material berkualitas tinggi dengan pengiriman yang tepat waktu. Kami sangat puas dengan profesionalisme dan dedikasi tim mereka.", "", 5, "from-red-500 to-pink-500", 1),
            ("Drs. Bambang Setiawan", "Project Manager", "CV. Bina Karya Utama", "Kerjasama dengan PT. Putra Syam Jaya sangat memuaskan. Tim mereka memiliki pemahaman mendalam tentang kebutuhan industri dan selalu menawarkan solusi inovatif.", "", 5, "from-blue-500 to-cyan-500", 2),
            ("Hj. Siti Rahmawati", "Procurement Manager", "PT. Nusantara Jaya", "CV. Asa Bangun Mandiri telah menjadi mitra terpercaya kami. Kualitas pekerjaan konstruksi mereka sangat baik dan harga yang kompetitif.", "", 5, "from-yellow-500 to-orange-500", 3),
        ]:
            cursor.execute(
                "INSERT INTO testimonials (name, position, company, content, image_url, rating, avatar_gradient, sort_order) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", t
            )

    # Clients
    cursor.execute("SELECT COUNT(*) AS c FROM clients")
    if cursor.fetchone()["c"] == 0:
        for c in [
            ("PT. Mega Infrastruktur", "", "bx-building", 1),
            ("CV. Bina Karya Utama", "", "bx-buildings", 2),
            ("PT. Nusantara Jaya", "", "bx-building-house", 3),
            ("PT. Maju Bersama", "", "bx-home-alt", 4),
            ("CV. Karya Mandiri", "", "bx-store", 5),
            ("PT. Sentosa Utama", "", "bx-cabinet", 6),
        ]:
            cursor.execute(
                "INSERT INTO clients (name, image_url, icon, sort_order) VALUES (%s,%s,%s,%s)", c
            )

    # Team members
    cursor.execute("SELECT COUNT(*) AS c FROM team_members")
    if cursor.fetchone()["c"] == 0:
        for t in [
            ("H. Muhammad Syam", "Direktur Utama", "Pemimpin visioner ASA Group dengan pengalaman lebih dari 15 tahun di bidang supplier dan kontraktor.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&q=80", "bx-user-circle", "from-purple-500 to-blue-500", 1),
            ("Ahmad Fauzi, ST", "Direktur Operasional", "Mengelola operasional harian dan memastikan kualitas layanan terjaga di semua lini perusahaan.", "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=300&q=80", "bx-user-circle", "from-red-500 to-pink-500", 2),
            ("Ir. Nurul Hidayat", "Manajer Proyek", "Ahli manajemen proyek dengan sertifikasi profesional dalam bidang konstruksi dan infrastruktur.", "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300&q=80", "bx-user-circle", "from-green-500 to-emerald-500", 3),
            ("Sari Dewi, SE", "Manajer Keuangan", "Bertanggung jawab atas perencanaan keuangan dan pengelolaan anggaran seluruh entitas grup.", "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=300&q=80", "bx-user-circle", "from-yellow-500 to-orange-500", 4),
        ]:
            cursor.execute(
                "INSERT INTO team_members (name, position, bio, image_url, icon, gradient, sort_order) VALUES (%s,%s,%s,%s,%s,%s,%s)", t
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
            ("Tips Memilih Material Konstruksi Berkualitas", "tips-memilih-material-konstruksi", "Panduan lengkap memilih material konstruksi yang tepat untuk proyek Anda.", "<h2>Panduan Memilih Material Konstruksi</h2><p>Memilih material konstruksi yang berkualitas adalah langkah krusial dalam setiap proyek pembangunan.</p><h3>1. Periksa Sertifikasi</h3><p>Pastikan material memiliki sertifikasi SNI untuk menjamin kualitas dan keamanan.</p><h3>2. Bandingkan Harga</h3><p>Jangan hanya tergiur harga murah. Bandingkan kualitas dan harga dari beberapa supplier.</p><h3>3. Cek Reputasi Supplier</h3><p>Pilih supplier berpengalaman dengan track record yang baik.</p><h3>4. Perhatikan Garansi</h3><p>Material berkualitas biasanya dilengkapi dengan garansi dari produsen.</p><h3>5. Konsultasi dengan Ahli</h3><p>Berkonsultasi dengan engineer untuk mendapatkan rekomendasi material terbaik sesuai kebutuhan proyek Anda.</p>", "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800&q=80", "bx-package", "from-red-500 to-orange-500", "Tips & Trik", "Admin"),
            ("Perkembangan Industri Konstruksi Indonesia 2024", "perkembangan-industri-konstruksi-2024", "Analisis tren dan perkembangan industri konstruksi di Indonesia.", "<h2>Tren Industri Konstruksi</h2><p>Industri konstruksi Indonesia terus menunjukkan pertumbuhan positif sepanjang tahun ini.</p><h3>1. Digitalisasi Konstruksi</h3><p>Penggunaan Building Information Modeling (BIM) semakin meluas di berbagai proyek besar.</p><h3>2. Green Building</h3><p>Kesadaran akan bangunan ramah lingkungan terus meningkat seiring regulasi pemerintah.</p><h3>3. Infrastruktur Prioritas</h3><p>Pemerintah terus mendorong pembangunan infrastruktur strategis di seluruh Indonesia.</p><h3>4. Material Inovatif</h3><p>Beton pracetak dan baja ringan semakin populer karena efisiensi waktu dan biaya.</p>", "https://images.unsplash.com/photo-1486325212027-8081e485255e?w=800&q=80", "bx-trending-up", "from-blue-500 to-cyan-500", "Industri", "Admin"),
            ("Pentingnya K3 dalam Proyek Konstruksi", "pentingnya-k3-proyek-konstruksi", "Memahami pentingnya Keselamatan dan Kesehatan Kerja dalam proyek konstruksi.", "<h2>Keselamatan dan Kesehatan Kerja</h2><p>K3 adalah aspek fundamental dalam setiap proyek konstruksi yang tidak boleh diabaikan.</p><h3>Mengapa K3 Penting?</h3><ul><li>Melindungi nyawa dan kesehatan pekerja</li><li>Meningkatkan produktivitas kerja</li><li>Mengurangi biaya akibat kecelakaan kerja</li><li>Memenuhi regulasi pemerintah</li></ul><h3>Implementasi K3 di ASA Group</h3><ol><li>Pelatihan K3 rutin untuk seluruh pekerja</li><li>Penyediaan APD standar di setiap lokasi proyek</li><li>Inspeksi berkala oleh tim HSE</li><li>Safety briefing harian sebelum memulai pekerjaan</li><li>Sistem pelaporan insiden yang transparan</li></ol>", "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800&q=80", "bx-shield-quarter", "from-green-500 to-emerald-500", "K3", "Admin"),
        ]:
            cursor.execute(
                "INSERT INTO blog_posts (title, slug, excerpt, content, image_url, cover_icon, cover_gradient, category, author) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", p
            )

    db.commit()
    cursor.close()
