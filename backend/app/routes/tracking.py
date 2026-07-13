from flask import Blueprint, request, jsonify
from app.database import bookings_col, tracking_col

tracking_bp = Blueprint('tracking', __name__)

@tracking_bp.route('/api/track/<awb_number>', methods=['GET'])
def track_parcel(awb_number):
    # First search for the booking reference
    booking = bookings_col.find_one({"awb": awb_number})
    
    if not booking:
        # Check if booking is pending without AWB
        return jsonify({
            "status": "Verification",
            "message": "Your booking request is under verification. Our team will contact you shortly."
        }), 404
        
    tracking_info = tracking_col.find_one({"awb": awb_number})
    
    return jsonify({
        "status": booking["status"],
        "awb": awb_number,
        "senderName": booking["sender"]["name"],
        "receiverName": booking["receiver"]["name"],
        "currentLocation": tracking_info.get("currentLocation", "Origin Hub") if tracking_info else "Processing",
        "estimatedDelivery": tracking_info.get("estimatedDelivery", "TBD") if tracking_info else "TBD",
        "timeline": tracking_info.get("timeline", []) if tracking_info else []
    }), 200
