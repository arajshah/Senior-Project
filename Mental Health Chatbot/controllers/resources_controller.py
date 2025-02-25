from flask import Blueprint, render_template
import json
import os

resources_bp = Blueprint("resources_bp", __name__)

@resources_bp.route("/resources", methods=["GET"])
def resources():
    resources_file = os.path.join("data", "resources.json")
    try:
        with open(resources_file, "r") as f:
            resources_data = json.load(f)
    except Exception as e:
        print("Error loading resources.json:", e)
        resources_data = []

    return render_template("resources.html", resources=resources_data)
