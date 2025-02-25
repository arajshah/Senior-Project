from flask import Blueprint, render_template

pages_bp = Blueprint("pages_bp", __name__)

@pages_bp.route("/")
def home():
    """
    Main landing page.
    """
    return render_template("landing.html")

# def chat_page():
#     """
#     Renders the chat page (GET).
#     The actual conversation is via /api/chat (POST).
#     """
#     return render_template("chat.html")

@pages_bp.route("/referral")
def referral_page():
    """
    Renders the referral page (GET).
    The actual search is via /api/find_professionals (POST).
    """
    return render_template("referral.html")

@pages_bp.route("/workplan")
def workplan_page():
    """
    Renders the personal work plan page (GET).
    The actual plan generation is /api/generate_workplan (POST).
    """
    return render_template("workplan.html")
