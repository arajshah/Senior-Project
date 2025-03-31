from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from db import db
from models.professional import Professional, Appointment
from datetime import datetime, timedelta

professional_bp = Blueprint("professional_bp", __name__)

# Professionals directory main page
@professional_bp.route("/", methods=["GET"])
def professionals_home():
    """
    Main professionals directory landing page
    """
    if not session.get("user_id"):
        return redirect(url_for("user_bp.login"))
    
    return render_template("professionals/professionals_home.html")

# Psychologists routes
@professional_bp.route("/psychologists", methods=["GET"])
def psychologists():
    """
    Display psychologists directory
    """
    if not session.get("user_id"):
        return redirect(url_for("user_bp.login"))
    
    psychologists = Professional.query.filter_by(profession="psychologist").all()
    return render_template("professionals/psychologists.html", professionals=psychologists)

# Psychiatrists routes
@professional_bp.route("/psychiatrists", methods=["GET"])
def psychiatrists():
    """
    Display psychiatrists directory
    """
    if not session.get("user_id"):
        return redirect(url_for("user_bp.login"))
    
    psychiatrists = Professional.query.filter_by(profession="psychiatrist").all()
    return render_template("professionals/psychiatrists.html", professionals=psychiatrists)

# Counselors routes
@professional_bp.route("/counselors", methods=["GET"])
def counselors():
    """
    Display counselors directory
    """
    if not session.get("user_id"):
        return redirect(url_for("user_bp.login"))
    
    counselors = Professional.query.filter_by(profession="counselor").all()
    return render_template("professionals/counselors.html", professionals=counselors)

# Professional detail page
@professional_bp.route("/professional/<int:professional_id>", methods=["GET"])
def professional_detail(professional_id):
    """
    Display details for a specific professional
    """
    if not session.get("user_id"):
        return redirect(url_for("user_bp.login"))
    
    professional = Professional.query.get_or_404(professional_id)
    
    # Get available appointment slots for the next 14 days
    today = datetime.now().date()
    two_weeks = today + timedelta(days=14)
    
    # In a real app, you'd query available slots from the database
    # For now, we'll just pass the professional to the template
    return render_template("professionals/professional_detail.html", professional=professional)

# Booking appointment route
@professional_bp.route("/book/<int:professional_id>", methods=["GET", "POST"])
def book_appointment(professional_id):
    """
    Book an appointment with a professional
    """
    if not session.get("user_id"):
        return redirect(url_for("user_bp.login"))
    
    professional = Professional.query.get_or_404(professional_id)
    
    if request.method == "POST":
        # In a real app, you'd handle the booking process here
        # For now, just redirect back to the professional's detail page
        return redirect(url_for("professional_bp.professional_detail", professional_id=professional_id))
    
    return render_template("professionals/booking.html", professional=professional)