# controllers/workplan_controller.py

from flask import Blueprint, request, jsonify
from services.deepseek_service import deepseek_service

workplan_bp = Blueprint("workplan_bp", __name__)

@workplan_bp.route("/generate_workplan", methods=["POST"])
def generate_workplan():
    mood = request.json.get("mood", "")
    goals = request.json.get("goals", "")

    prompt = (
        f"You are an empathetic mental health assistant named Aurora. "
        f"The user is feeling '{mood}' and their goals are: {goals}. "
        "Generate a comprehensive mental health work plan with daily self-care tasks, "
        "mindfulness exercises, and weekly progress checkpoints."
    )

    plan_response = deepseek_service.query_deepseek(prompt)
    return jsonify({"workplan": plan_response})
