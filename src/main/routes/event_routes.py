from flask import Blueprint, jsonify, request
from src.http_types.http_request import HttpRequest
from src.data.event_handler import EventHandler
from src.errors.error_handler import handle_error

event_rout_bp = Blueprint("event_route", __name__)

@event_rout_bp.route("/events", methods=["POST"])
def create_event():
    try:
        http_request = HttpRequest(body=request.json)
        event_handler = EventHandler()
        
        
        http_response = event_handler.register(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code
    
@event_rout_bp.route("/events/<event_id>", methods=["GET"])
def get_event(event_id):
    try:    
        event_handler = EventHandler()
        http_request = HttpRequest(param={"event_id": event_id})
        http_response = event_handler.find_by_id(http_request)
        
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code
    
@event_rout_bp.route("/events/<event_id>/exclude_event", methods=["GET"])
def exclude_event(event_id):
    try:    
        event_handler = EventHandler()
        http_request = HttpRequest(param={"event_id": event_id})
        http_response = event_handler.exclude_event(http_request)
        
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code

@event_rout_bp.route("/events/<event_id>/update_event", methods=["POST"])
def update_event(event_id):
    try:    
        event_handler = EventHandler()
        http_request = HttpRequest(param={"event_id": event_id}, body=request.json)
        http_response = event_handler.update_event(http_request)
        
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_error(exception)
        return jsonify(http_response.body), http_response.status_code
        