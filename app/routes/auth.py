"""Authentication routes."""

import hashlib

from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from app.extensions import get_db

auth_bp = Blueprint("auth", __name__, url_prefix="/admin")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        pw_hash = hashlib.sha256(password.encode()).hexdigest()
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username=%s AND password_hash=%s",
            (username, pw_hash),
        )
        user = cur.fetchone()
        cur.close()
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Login berhasil!", "success")
            return redirect(url_for("admin.dashboard"))
        flash("Username atau password salah.", "error")
    return render_template("admin/login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logout berhasil.", "success")
    return redirect(url_for("auth.login"))
