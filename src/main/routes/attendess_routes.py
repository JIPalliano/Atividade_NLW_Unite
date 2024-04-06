from flask import Blueprint, jsonify, request
from src.http_types.http_request import HttpRequest
from src.data.attendees_handler import AttendeesHandler
from src.errors.error_handler import handle_error

attendees_route_bp = Blueprint("attendees_route",__name__)

@attendees_route_bp.route("/events/<event_id>/register", methods=["POST"])
def create_attendees(event_id):
    try:
        attendees_handler = AttendeesHandler()
        http_request = HttpRequest(param={"event_id": event_id}, body=request.json)
        
        http_response = attendees_handler.registry(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code

@attendees_route_bp.route("/attendees/<attendees_id>/badge", methods=["GET"])
def get_attendees_badge(attendees_id):
    try:
        attendees_handler = AttendeesHandler()
        http_request = HttpRequest(param={"attendees_id": attendees_id})
        
        http_response = attendees_handler.find_attendees_badge(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code

@attendees_route_bp.route("/events/<event_id>/attendees", methods=["GET"])
def get_attendees(event_id):
    try:
        attendees_handler = AttendeesHandler()
        http_request = HttpRequest(param={"event_id": event_id})
        
        http_response = attendees_handler.find_attendees_from_event(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code
    
@attendees_route_bp.route("/attendees/<attendees_id>/exclude_attendees", methods=["GET"])
def exclude_attendees(attendees_id):
    try:
        attendees_handler = AttendeesHandler()
        http_request = HttpRequest(param={"attendees_id": attendees_id})
        
        http_response = attendees_handler.exclude_attendees(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code
    
@attendees_route_bp.route("/attendees/<attendees_id>/update_attendees", methods=["POST"])
def update_attendees(attendees_id):
    try:
        attendees_handler = AttendeesHandler()
        http_request = HttpRequest(param={"attendees_id": attendees_id}, body=request.json)
        
        http_response = attendees_handler.update_attendees(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code