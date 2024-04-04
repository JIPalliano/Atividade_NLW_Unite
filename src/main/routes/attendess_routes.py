from flask import Blueprint, jsonify, request
from src.http_types.http_request import HttpRequest
from src.data.attendees_handler import AttendeesHandler

attendees_route_bp = Blueprint("attendees_route",__name__)

@attendees_route_bp.route("/events/<event_id>/register", methods=["POST"])
def create_attendees(event_id):
    attendees_handler = AttendeesHandler()
    http_request = HttpRequest(param={"event_id": event_id}, body=request.json)
    
    http_response = attendees_handler.registry(http_request)
    return jsonify(http_response.body), http_response.status_code