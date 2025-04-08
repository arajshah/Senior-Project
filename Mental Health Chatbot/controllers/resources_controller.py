from flask import Blueprint, render_template, abort, request, redirect, url_for, session
import json
import os

resources_bp = Blueprint("resources_bp", __name__)

def load_resources():
    """Helper function to load resources from JSON file"""
    resources_file = os.path.join("data", "resources.json")
    try:
        with open(resources_file, "r") as f:
            resources_data = json.load(f)
    except Exception as e:
        print("Error loading resources.json:", e)
        resources_data = []
    
    return resources_data

@resources_bp.route("/resources", methods=["GET"])
def resources():
    """Display resources page"""
    resources_data = load_resources()
    return render_template("resources.html", resources=resources_data)

@resources_bp.route("/all-resources", methods=["GET"])
def all_resources():
    """Display all resources page (could be same as resources or a different view)"""
    # This can be the same as resources() if you want
    resources_data = load_resources()
    return render_template("all_resources.html", resources=resources_data)

@resources_bp.route("/resource/<int:resource_id>", methods=["GET"])
def view_resource(resource_id):
    """View a specific resource"""
    resources_data = load_resources()
    
    # Find the resource with the matching ID
    resource = next((r for r in resources_data if r.get('id') == resource_id), None)
    
    if not resource:
        abort(404)  # Resource not found
    
    return render_template("resource_detail.html", resource=resource)

@resources_bp.route("/bookmarked", methods=["GET"])
def bookmarked_resources():
    """View bookmarked resources"""
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("user_bp.login"))
    
    # In a real app, you would load bookmarked resources from database
    # For now, we'll just show all resources
    resources_data = load_resources()
    
    return render_template("bookmarked_resources.html", resources=resources_data)