from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, Response
import json
from services.deepseek_service import deepseek_service
from models.conversation import Conversation
from db import db

conversation_bp = Blueprint("conversation_bp", __name__)

@conversation_bp.route("/chat", methods=["GET"])
def chat_page():
    if not session.get("user_id"):
        return redirect(url_for("user_bp.login"))
    return render_template("chat.html")

@conversation_bp.route("/chat/send", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # Get user_id from session
    user_id = session.get("user_id")

    def generate():
        full_response = ""
        for chunk in deepseek_service.query_deepseek_stream(user_message):
            full_response += chunk
            yield f"data: {json.dumps({'chunk': chunk})}\n\n"

        # Store conversation after complete response
        if user_id:
            conversation = Conversation(
                user_id=user_id,
                user_message=user_message,
                assistant_response=full_response.strip()
            )
            db.session.add(conversation)
            db.session.commit()

    return Response(generate(), mimetype='text/event-stream')