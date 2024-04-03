from flask import Blueprint, jsonify

event_rout_bp = Blueprint("event_route", __name__)

@event_rout_bp.route("/events", methods=["POST"])
def create_event():
    return jsonify({"olá": "mundo"}), 200