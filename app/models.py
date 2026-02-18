"""Database schema initialization for MySQL."""

from app.extensions import get_db


def init_tables():
    """Create all required tables if they don't exist."""
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        role VARCHAR(50) DEFAULT 'admin'
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS site_settings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        setting_key VARCHAR(100) UNIQUE NOT NULL,
        setting_value TEXT
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS blog_posts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        slug VARCHAR(255) UNIQUE NOT NULL,
        excerpt TEXT,
        content LONGTEXT NOT NULL,
        image_url VARCHAR(500) DEFAULT '',
        cover_icon VARCHAR(100) DEFAULT 'bx-news',
        cover_gradient VARCHAR(100) DEFAULT 'from-purple-600 to-blue-600',
        category VARCHAR(100) DEFAULT 'Umum',
        author VARCHAR(100) DEFAULT 'Admin',
        status VARCHAR(50) DEFAULT 'published',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS services (
        id INT AUTO_INCREMENT PRIMARY KEY,
        icon VARCHAR(100) DEFAULT 'bx-cog',
        title VARCHAR(255) NOT NULL,
        description TEXT,
        image_url VARCHAR(500) DEFAULT '',
        gradient VARCHAR(100) DEFAULT 'from-purple-500 to-blue-500',
        sort_order INT DEFAULT 0
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gallery_items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        company VARCHAR(255),
        category VARCHAR(100),
        image_url VARCHAR(500) DEFAULT '',
        icon VARCHAR(100) DEFAULT 'bx-building',
        gradient VARCHAR(100) DEFAULT 'from-purple-600 to-blue-600',
        sort_order INT DEFAULT 0
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS testimonials (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        position VARCHAR(255),
        company VARCHAR(255),
        content TEXT NOT NULL,
        image_url VARCHAR(500) DEFAULT '',
        rating INT DEFAULT 5,
        avatar_gradient VARCHAR(100) DEFAULT 'from-purple-500 to-blue-500',
        sort_order INT DEFAULT 0
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        image_url VARCHAR(500) DEFAULT '',
        icon VARCHAR(100) DEFAULT 'bx-building',
        sort_order INT DEFAULT 0
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS team_members (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        position VARCHAR(255),
        bio TEXT,
        image_url VARCHAR(500) DEFAULT '',
        icon VARCHAR(100) DEFAULT 'bx-user',
        gradient VARCHAR(100) DEFAULT 'from-purple-500 to-blue-500',
        sort_order INT DEFAULT 0
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faqs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        sort_order INT DEFAULT 0
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        slug VARCHAR(255) UNIQUE NOT NULL,
        tagline VARCHAR(255) DEFAULT '',
        description TEXT,
        logo_url VARCHAR(500) DEFAULT '',
        icon VARCHAR(100) DEFAULT 'bx-buildings',
        color_primary VARCHAR(50) DEFAULT '#7C3AED',
        color_secondary VARCHAR(50) DEFAULT '#2563EB',
        color_tertiary VARCHAR(50) DEFAULT '#1e1b4b',
        gradient VARCHAR(200) DEFAULT 'from-purple-600 to-blue-600',
        gradient_short VARCHAR(200) DEFAULT 'from-purple-600 to-blue-600',
        bg_class VARCHAR(100) DEFAULT 'bg-purple-600',
        bg_secondary_class VARCHAR(100) DEFAULT 'bg-blue-600',
        text_class VARCHAR(100) DEFAULT 'text-purple-600',
        text_secondary_class VARCHAR(100) DEFAULT 'text-blue-600',
        border_class VARCHAR(100) DEFAULT 'border-purple-600',
        ring_class VARCHAR(100) DEFAULT 'ring-purple-600',
        founded VARCHAR(20) DEFAULT '',
        specialties TEXT,
        sort_order INT DEFAULT 0
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)

    # Add image_url columns if they don't exist (migration for existing DBs)
    _add_column_if_missing(cursor, "blog_posts", "image_url", "VARCHAR(500) DEFAULT ''")
    _add_column_if_missing(cursor, "services", "image_url", "VARCHAR(500) DEFAULT ''")
    _add_column_if_missing(cursor, "gallery_items", "image_url", "VARCHAR(500) DEFAULT ''")
    _add_column_if_missing(cursor, "testimonials", "image_url", "VARCHAR(500) DEFAULT ''")
    _add_column_if_missing(cursor, "clients", "image_url", "VARCHAR(500) DEFAULT ''")
    _add_column_if_missing(cursor, "team_members", "image_url", "VARCHAR(500) DEFAULT ''")

    db.commit()
    cursor.close()


def _add_column_if_missing(cursor, table, column, col_def):
    """Add a column to a table if it doesn't already exist."""
    cursor.execute(
        "SELECT COUNT(*) AS c FROM information_schema.COLUMNS "
        "WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME=%s AND COLUMN_NAME=%s",
        (table, column),
    )
    if cursor.fetchone()["c"] == 0:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_def}")
