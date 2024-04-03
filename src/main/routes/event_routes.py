from flask import Blueprint, jsonify, request
from src.http_types.http_request import HttpResquest

event_rout_bp = Blueprint("event_route", __name__)

@event_rout_bp.route("/events", methods=["POST"])
def create_event():
    http_request = HttpResquest(body=request.json)
    
    
    return jsonify({"olá": "mundo"}), 200