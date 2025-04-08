from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from db import db
from models.journal import Journal
from models.goal import Goal  # Import the new Goal model
from datetime import datetime, timedelta

journal_bp = Blueprint("journal_bp", __name__)

@journal_bp.route("/journal", methods=["GET"])
def journal():
    """Render the journal page"""
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("user_bp.login"))
    
    entries = Journal.query.filter_by(user_id=user_id).order_by(Journal.timestamp.desc()).all()
    return render_template("journal.html", entries=entries)

@journal_bp.route("/new-entry", methods=["GET", "POST"])
def new_entry():
    """Render the new journal entry page and handle form submission"""
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("user_bp.login"))
    
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        
        if not title or not content:
            return "Title and content are required", 400
            
        new_entry = Journal(user_id, title, content)
        db.session.add(new_entry)
        db.session.commit()
        
        return redirect(url_for("journal_bp.journal"))
        
    return render_template("new_journal_entry.html")

@journal_bp.route("/journal/add", methods=["POST"])
def add_journal():
    """Add a new journal entry via AJAX"""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "You must be logged in to create journal entries"}), 401
    
    # Check if JSON or form data
    if request.is_json:
        data = request.json
        title = data.get("title")
        content = data.get("content")
    else:
        title = request.form.get("title")
        content = request.form.get("content")
    
    # Validate data
    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400
    
    # Create new entry
    new_entry = Journal(user_id, title, content)
    db.session.add(new_entry)
    db.session.commit()
    
    # Return the created entry for AJAX requests
    return jsonify({
        "success": True,
        "message": "Journal entry created successfully",
        "entry": {
            "id": new_entry.id,
            "title": new_entry.title,
            "content": new_entry.content,
            "timestamp": new_entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
    })

@journal_bp.route("/journal/edit/<int:entry_id>", methods=["PUT"])
def edit_journal(entry_id):
    """Edit an existing journal entry"""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "You must be logged in to edit journal entries"}), 401
    
    # Get entry
    entry = Journal.query.filter_by(id=entry_id, user_id=user_id).first()
    if not entry:
        return jsonify({"error": "Journal entry not found or access denied"}), 404
    
    # Get data
    data = request.json
    title = data.get("title")
    content = data.get("content")
    
    # Validate data
    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400
    
    # Update entry
    entry.title = title
    entry.content = content
    db.session.commit()
    
    # Return updated entry
    return jsonify({
        "success": True,
        "message": "Journal entry updated successfully",
        "entry": {
            "id": entry.id,
            "title": entry.title,
            "content": entry.content,
            "timestamp": entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
    })

@journal_bp.route("/journal/delete/<int:entry_id>", methods=["DELETE"])
def delete_journal(entry_id):
    """Delete a journal entry"""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "You must be logged in to delete journal entries"}), 401
    
    # Get entry
    entry = Journal.query.filter_by(id=entry_id, user_id=user_id).first()
    if not entry:
        return jsonify({"error": "Journal entry not found or access denied"}), 404
    
    # Delete entry
    db.session.delete(entry)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Journal entry deleted successfully"
    })

@journal_bp.route("/journal/stats", methods=["GET"])
def journal_stats():
    """Get journal statistics"""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "You must be logged in to view statistics"}), 401
    
    # Get all entries
    entries = Journal.query.filter_by(user_id=user_id).order_by(Journal.timestamp.desc()).all()
    
    # Calculate streak
    streak = calculate_streak(entries, user_id)
    
    # Return stats
    return jsonify({
        "entry_count": len(entries),
        "streak": streak,
        "latest_entry": entries[0].timestamp.strftime("%Y-%m-%d") if entries else None
    })

@journal_bp.route("/prompts", methods=["GET"])
def prompts():
    """Render the journal prompts page"""
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("user_bp.login"))
    
    # Sample prompts that could be moved to a database
    journal_prompts = [
        "What are three things you're grateful for today?",
        "Describe a challenge you're facing and three possible ways to address it.",
        "What made you smile today?",
        "Reflect on a recent accomplishment. What did you learn from it?",
        "What are you looking forward to this week?",
        "Describe a moment when you felt proud of yourself recently.",
        "What self-care activities could you prioritize today?",
        "Write about a concern that's been weighing on your mind.",
        "What boundaries do you need to set or maintain for your mental health?",
        "Describe your ideal day. What would you do and how would you feel?"
    ]
    
    return render_template("journal_prompts.html", prompts=journal_prompts)

@journal_bp.route("/goals", methods=["GET", "POST"])
def goals():
    """Render the goals page and handle form submission"""
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("user_bp.login"))
    
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description", "")
        due_date_str = request.form.get("due_date")
        
        if not title or not due_date_str:
            return "Title and due date are required", 400
            
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
            new_goal = Goal(user_id, title, due_date, description)
            db.session.add(new_goal)
            db.session.commit()
            return redirect(url_for("journal_bp.goals"))
        except ValueError:
            return "Invalid date format", 400
    
    # Get all user goals
    goals = Goal.query.filter_by(user_id=user_id).order_by(Goal.due_date).all()
    return render_template("goals.html", goals=goals)

@journal_bp.route("/goals/toggle/<int:goal_id>", methods=["POST"])
def toggle_goal(goal_id):
    """Toggle a goal's completion status"""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "You must be logged in to update goals"}), 401
    
    # Get goal
    goal = Goal.query.filter_by(id=goal_id, user_id=user_id).first()
    if not goal:
        return jsonify({"error": "Goal not found or access denied"}), 404
    
    # Toggle status
    goal.completed = not goal.completed
    db.session.commit()
    
    return jsonify({
        "success": True,
        "completed": goal.completed
    })

def calculate_streak(entries, user_id):
    """Calculate the current journaling streak"""
    if not entries:
        return 0
    
    # Get latest entry date
    latest = entries[0].timestamp.date()
    today = datetime.now().date()
    
    # If latest entry is not from today or yesterday, streak is broken
    if (today - latest).days > 1:
        return 0
    
    # Count consecutive days backward from latest entry
    streak = 1  # Start with 1 for the latest entry day
    current_date = latest - timedelta(days=1)  # Start checking from the day before latest
    
    # Check each day backward until we find a gap
    while True:
        # Check if there's any entry on this date
        entries_on_date = Journal.query.filter(
            Journal.user_id == user_id,
            db.func.date(Journal.timestamp) == current_date
        ).first()
        
        if not entries_on_date:
            break  # Gap found, end of streak
        
        streak += 1
        current_date -= timedelta(days=1)
    
    return streak