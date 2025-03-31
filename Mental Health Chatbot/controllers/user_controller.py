from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from db import db
from models.user import User
from models.conversation import Conversation
from models.mood import Mood
from models.journal import Journal
from datetime import datetime, timedelta

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing_user:
            return "Username or email is already taken.", 400

        new_user = User(username, email, password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("user_bp.login"))

    return render_template("register.html")

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print("We are here")
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("user_bp.dashboard"))
        else:
            return "Invalid credentials.", 401

    print("We are out here")
    return render_template("login.html")

@user_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("user_bp.login"))

@user_bp.route("/dashboard")
def dashboard():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("user_bp.login"))

    # Calculate days active (from first activity)
    first_activity = min(
        Conversation.query.filter_by(user_id=user_id).first().timestamp if Conversation.query.filter_by(user_id=user_id).first() else datetime.now(),
        Mood.query.filter_by(user_id=user_id).first().timestamp if Mood.query.filter_by(user_id=user_id).first() else datetime.now(),
        Journal.query.filter_by(user_id=user_id).first().timestamp if Journal.query.filter_by(user_id=user_id).first() else datetime.now(),
    )
    days_active = (datetime.now() - first_activity).days + 1

    # Get activity counts
    stats = {
        'days_active': days_active,
        'chat_count': Conversation.query.filter_by(user_id=user_id).count(),
        'mood_entries': Mood.query.filter_by(user_id=user_id).count(),
        'journal_count': Journal.query.filter_by(user_id=user_id).count()
    }

    return render_template("dashboard.html", **stats)