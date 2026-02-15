from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    """Landing page for ASA Group."""
    companies = [
        {
            "name": "PT. Nur Putra Mandiri",
            "slug": "nur-putra-mandiri",
            "tagline": "Keunggulan dalam Setiap Solusi",
            "colors": {"primary": "#DC2626", "secondary": "#16A34A", "gradient": "from-red-600 to-green-600"},
            "description": (
                "Perusahaan yang bergerak dalam bidang perdagangan umum dan jasa, "
                "mengutamakan profesionalitas dan kualitas tinggi dalam setiap proyek."
            ),
            "icon": "bx-buildings",
        },
        {
            "name": "PT. Putra Syam Jaya",
            "slug": "putra-syam-jaya",
            "tagline": "Inovasi Tanpa Batas",
            "colors": {"primary": "#7C3AED", "secondary": "#2563EB", "gradient": "from-violet-600 to-blue-600"},
            "description": (
                "Mitra terpercaya dalam pengadaan bahan dan peralatan industri "
                "dengan standar kualitas internasional."
            ),
            "icon": "bx-cube-alt",
        },
        {
            "name": "CV. Asa Bangun Mandiri",
            "slug": "asa-bangun-mandiri",
            "tagline": "Membangun Masa Depan",
            "colors": {"primary": "#DC2626", "secondary": "#F59E0B", "gradient": "from-red-600 to-yellow-500"},
            "description": (
                "Kontraktor handal dengan dedikasi tinggi dalam pembangunan "
                "infrastruktur dan proyek konstruksi."
            ),
            "icon": "bx-hard-hat",
        },
    ]
    return render_template("index.html", companies=companies)


@app.route("/company/<slug>")
def company(slug):
    """Individual company profile page."""
    companies_data = {
        "nur-putra-mandiri": {
            "name": "PT. Nur Putra Mandiri",
            "slug": "nur-putra-mandiri",
            "tagline": "Keunggulan dalam Setiap Solusi",
            "colors": {
                "primary": "#DC2626",
                "secondary": "#16A34A",
                "gradient": "from-red-600 to-green-600",
                "bg": "bg-red-600",
                "bg_secondary": "bg-green-600",
                "text": "text-red-600",
                "text_secondary": "text-green-600",
                "border": "border-red-600",
                "ring": "ring-red-600",
            },
            "description": (
                "PT. Nur Putra Mandiri merupakan perusahaan swasta yang bergerak dalam "
                "bidang perdagangan umum dan jasa sebagai General Supplier & Kontraktor. "
                "Kami selalu menekankan pada aspek profesionalitas, berorientasi pada "
                "kualitas dan ketepatan waktu dalam melayani kebutuhan pelanggan."
            ),
            "founded": "2018",
            "specialties": [
                "Pengadaan Material Konstruksi",
                "Supplier Peralatan Industri",
                "Jasa Konstruksi Bangunan",
                "Renovasi & Pemeliharaan",
            ],
            "icon": "bx-buildings",
        },
        "putra-syam-jaya": {
            "name": "PT. Putra Syam Jaya",
            "slug": "putra-syam-jaya",
            "tagline": "Inovasi Tanpa Batas",
            "colors": {
                "primary": "#7C3AED",
                "secondary": "#2563EB",
                "gradient": "from-violet-600 to-blue-600",
                "bg": "bg-violet-600",
                "bg_secondary": "bg-blue-600",
                "text": "text-violet-600",
                "text_secondary": "text-blue-600",
                "border": "border-violet-600",
                "ring": "ring-violet-600",
            },
            "description": (
                "PT. Putra Syam Jaya merupakan perusahaan swasta yang bergerak dalam "
                "bidang perdagangan umum dan jasa sebagai General Supplier & Kontraktor. "
                "Kami menjadi mitra terpercaya dalam pengadaan bahan dan peralatan "
                "industri dengan standar kualitas internasional."
            ),
            "founded": "2019",
            "specialties": [
                "Supplier Peralatan Berat",
                "Pengadaan Bahan Bangunan",
                "Konsultasi Proyek",
                "Manajemen Konstruksi",
            ],
            "icon": "bx-cube-alt",
        },
        "asa-bangun-mandiri": {
            "name": "CV. Asa Bangun Mandiri",
            "slug": "asa-bangun-mandiri",
            "tagline": "Membangun Masa Depan",
            "colors": {
                "primary": "#DC2626",
                "secondary": "#F59E0B",
                "gradient": "from-red-600 to-yellow-500",
                "bg": "bg-red-600",
                "bg_secondary": "bg-yellow-500",
                "text": "text-red-600",
                "text_secondary": "text-yellow-500",
                "border": "border-red-600",
                "ring": "ring-red-600",
            },
            "description": (
                "CV. Asa Bangun Mandiri merupakan perusahaan swasta yang bergerak dalam "
                "bidang perdagangan umum dan jasa sebagai General Supplier & Kontraktor. "
                "Kami hadir sebagai kontraktor handal dengan dedikasi tinggi dalam "
                "pembangunan infrastruktur dan proyek konstruksi."
            ),
            "founded": "2020",
            "specialties": [
                "Konstruksi Infrastruktur",
                "Pembangunan Gedung",
                "Supplier Material Premium",
                "Jasa Perawatan Fasilitas",
            ],
            "icon": "bx-hard-hat",
        },
    }

    company_data = companies_data.get(slug)
    if not company_data:
        return render_template("404.html"), 404

    return render_template("company.html", company=company_data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
