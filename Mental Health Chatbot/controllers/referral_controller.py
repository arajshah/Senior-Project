from flask import Blueprint, request, jsonify
import json

referral_bp = Blueprint("referral_bp", __name__)

@referral_bp.route("/find_professionals", methods=["POST"])
def find_professionals():
    location = request.json.get("location", "")
    specialty = request.json.get("specialty", "")

    try:
        with open("data/professionals.json", "r") as f:
            professionals = json.load(f)
    except Exception as e:
        print("Error loading professionals data:", e)
        return jsonify({"error": "Unable to load professionals data."}), 500

    filtered = [
        prof for prof in professionals
        if location.lower() in prof.get("location", "").lower()
           and specialty.lower() in prof.get("specialty", "").lower()
    ]
    return jsonify({"professionals": filtered})
