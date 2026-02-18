# ASA Group — Company Profile Website

Modern company profile website for **ASA Group**, a collection of General Supplier & Kontraktor companies built with **Flask** and **Tailwind CSS**.

## Companies

- **PT. Nur Putra Mandiri** — General Supplier (Red & Green branding)
- **PT. Putra Syam Jaya** — Supplier & Kontraktor (Blue & Violet branding)
- **CV. Asa Bangun Mandiri** — Kontraktor (Red & Yellow branding)

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: Tailwind CSS (CDN), Boxicons
- **Fonts**: Inter, Poppins (Google Fonts)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

## Project Structure

```
ASA/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   ├── base.html          # Base template with navigation & footer
│   ├── index.html         # Main landing page
│   ├── company.html       # Individual company profile page
│   └── 404.html           # Error page
└── static/
    ├── css/
    ├── js/
    └── img/
```

## Features

- Responsive design with modern glassmorphism effects
- Animated sections with scroll-reveal
- Company profile pages for each subsidiary
- About, Vision & Mission, Services, Gallery, Testimonials, Client, and CSR sections
- Marketing-oriented CTAs and contact sections
- Boxicons integration for all icons