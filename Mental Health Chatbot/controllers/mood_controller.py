from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from db import db
from models.mood import Mood
from datetime import datetime, timedelta

# Create blueprint without url_prefix to maintain /mood route
mood_bp = Blueprint("mood_bp", __name__)

@mood_bp.route("/mood", methods=["GET"])
def mood():
    """
    Render the mood tracking page
    """
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("user_bp.login"))
    return render_template("mood.html")

@mood_bp.route("/mood/add", methods=["POST"])
def add_mood():
    """
    Add a new mood entry via API for AJAX requests
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "You must be logged in to track your mood"}), 401
    
    data = request.json
    
    # Validate mood data
    mood_value = data.get("mood_value")
    note = data.get("note", "")
    
    if not mood_value:
        return jsonify({"error": "Mood value is required"}), 400
    
    try:
        mood_value = int(mood_value)
        if mood_value < 1 or mood_value > 10:
            return jsonify({"error": "Mood value must be between 1 and 10"}), 400
    except ValueError:
        return jsonify({"error": "Mood value must be a number"}), 400
    
    # Create new mood entry
    new_mood = Mood(
        user_id=user_id,
        score=mood_value,  # Match the model field name 'score'
        note=note
    )
    
    # Save to database
    db.session.add(new_mood)
    db.session.commit()
    
    return jsonify({"success": True, "message": "Mood saved successfully"}), 201

@mood_bp.route("/mood/data", methods=["GET"])
def mood_data():
    """
    Get mood data for the logged in user
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    # Get all entries for user, ordered by timestamp
    entries = Mood.query.filter_by(user_id=user_id).order_by(Mood.timestamp).all()
    
    # Format for JSON response, mapping 'score' to 'mood_value' for JS compatibility
    data = []
    for entry in entries:
        data.append({
            "id": entry.id,
            "timestamp": entry.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "mood_value": entry.score,  # Map score to mood_value for JS
            "note": entry.note
        })
        
    return jsonify(data)

@mood_bp.route("/mood/stats", methods=["GET"])
def mood_stats():
    """
    Get mood statistics for the logged in user
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
    
    # Filter by time range if specified
    time_range = request.args.get("range", "all")
    
    # Get base query
    query = Mood.query.filter_by(user_id=user_id)
    
    # Apply time filter
    now = datetime.utcnow()
    if time_range == "week":
        start_date = now - timedelta(days=7)
        query = query.filter(Mood.timestamp >= start_date)
    elif time_range == "month":
        start_date = now - timedelta(days=30)
        query = query.filter(Mood.timestamp >= start_date)
    
    # Get entries
    entries = query.all()
    
    if not entries:
        return jsonify({
            "count": 0,
            "average": None,
            "highest": None,
            "lowest": None,
            "most_recent": None
        })
    
    # Calculate stats
    mood_values = [entry.score for entry in entries]
    
    # Get most recent entry
    most_recent = max(entries, key=lambda entry: entry.timestamp)
    
    stats = {
        "count": len(entries),
        "average": sum(mood_values) / len(mood_values),
        "highest": max(mood_values),
        "lowest": min(mood_values),
        "most_recent": {
            "timestamp": most_recent.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "mood_value": most_recent.score,
            "note": most_recent.note
        }
    }
    
    return jsonify(stats)