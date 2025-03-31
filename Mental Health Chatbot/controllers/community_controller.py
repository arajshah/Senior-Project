from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from db import db
from models.community import Forum, ForumPost, SupportGroup, Event
from datetime import datetime

community_bp = Blueprint("community_bp", __name__)

# Forum routes
@community_bp.route("/forums", methods=["GET"])
def forums():
    """
    Display discussion forums
    """
    if not session.get("user_id"):
        return redirect(url_for("user_bp.login"))
    
    # Get all forums
    forums = Forum.query.all()
    return render_template("community/forums.html", forums=forums)

@community_bp.route("/forums/<int:forum_id>", methods=["GET"])
def forum_detail(forum_id):
    """
    Display a specific forum with its posts
    """
    if not session.get("user_id"):
        return redirect(url_for("user_bp.login"))
    
    forum = Forum.query.get_or_404(forum_id)
    posts = ForumPost.query.filter_by(forum_id=forum_id).all()
    return render_template("community/forum_detail.html", forum=forum, posts=posts)

# Support Groups routes
@community_bp.route("/groups", methods=["GET"])
def groups():
    """
    Display support groups
    """
    if not session.get("user_id"):
        return redirect(url_for("user_bp.login"))
    
    groups = SupportGroup.query.all()
    return render_template("community/groups.html", groups=groups)

@community_bp.route("/groups/<int:group_id>", methods=["GET"])
def group_detail(group_id):
    """
    Display details for a specific support group
    """
    if not session.get("user_id"):
        return redirect(url_for("user_bp.login"))
    
    group = SupportGroup.query.get_or_404(group_id)
    return render_template("community/group_detail.html", group=group)

# Events routes
@community_bp.route("/events", methods=["GET"])
def events():
    """
    Display virtual events
    """
    if not session.get("user_id"):
        return redirect(url_for("user_bp.login"))
    
    upcoming_events = Event.query.filter(Event.date >= datetime.now()).order_by(Event.date).all()
    past_events = Event.query.filter(Event.date < datetime.now()).order_by(Event.date.desc()).all()
    return render_template("community/events.html", upcoming_events=upcoming_events, past_events=past_events)

@community_bp.route("/events/<int:event_id>", methods=["GET"])
def event_detail(event_id):
    """
    Display details for a specific event
    """
    if not session.get("user_id"):
        return redirect(url_for("user_bp.login"))
    
    event = Event.query.get_or_404(event_id)
    return render_template("community/event_detail.html", event=event)

# Community home
@community_bp.route("/", methods=["GET"])
def community_home():
    """
    Main community landing page
    """
    if not session.get("user_id"):
        return redirect(url_for("user_bp.login"))
    
    forums = Forum.query.limit(3).all()
    groups = SupportGroup.query.limit(3).all()
    upcoming_events = Event.query.filter(Event.date >= datetime.now()).order_by(Event.date).limit(3).all()
    
    return render_template("community/community_home.html", 
                           forums=forums, 
                           groups=groups, 
                           events=upcoming_events)