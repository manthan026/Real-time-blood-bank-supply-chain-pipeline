"""
This file contains the schema (structure) for every event
generated in the Blood Bank Supply Chain Management System.

All events share a common structure:
1. Common fields
2. Event-specific fields
"""

# Common fields present in every event
COMMON_FIELDS = [
    "event_id",
    "event_type",
    "timestamp",
    "blood_bank",
    "city",
    "state"
]


# Donation Event
DONATION_SCHEMA = {
    "event_id": "",
    "event_type": "donation",
    "timestamp": "",
    "blood_bank": "",
    "city": "",
    "state": "",

    "donor_id": "",
    "donor_name": "",
    "age": 0,
    "gender": "",
    "blood_group": "",
    "component": "",
    "units_donated": 0,
    "donation_status": ""
}


# Blood Request Event
REQUEST_SCHEMA = {
    "event_id": "",
    "event_type": "request",
    "timestamp": "",
    "blood_bank": "",
    "city": "",
    "state": "",

    "request_id": "",
    "hospital_name": "",
    "blood_group": "",
    "component": "",
    "units_requested": 0,
    "priority": "",
    "request_status": ""
}


# Blood Screening Event
SCREENING_SCHEMA = {
    "event_id": "",
    "event_type": "screening",
    "timestamp": "",
    "blood_bank": "",
    "city": "",
    "state": "",

    "screening_id": "",
    "donor_id": "",
    "blood_group": "",
    "screening_status": "",
    "remarks": ""
}


# Blood Transfer Event
TRANSFER_SCHEMA = {
    "event_id": "",
    "event_type": "transfer",
    "timestamp": "",
    "blood_bank": "",
    "city": "",
    "state": "",

    "transfer_id": "",
    "source_bank": "",
    "destination_bank": "",
    "blood_group": "",
    "component": "",
    "units_transferred": 0,
    "transfer_status": ""
}


# Blood Dispatch Event
DISPATCH_SCHEMA = {
    "event_id": "",
    "event_type": "dispatch",
    "timestamp": "",
    "blood_bank": "",
    "city": "",
    "state": "",

    "dispatch_id": "",
    "hospital_name": "",
    "blood_group": "",
    "component": "",
    "units_dispatched": 0,
    "dispatch_status": ""
}


# Inventory Event
INVENTORY_SCHEMA = {
    "event_id": "",
    "event_type": "inventory",
    "timestamp": "",
    "blood_bank": "",
    "city": "",
    "state": "",

    "inventory_id": "",
    "blood_group": "",
    "component": "",
    "available_units": 0,
    "inventory_status": ""
}


# Expiry Event
EXPIRY_SCHEMA = {
    "event_id": "",
    "event_type": "expiry",
    "timestamp": "",
    "blood_bank": "",
    "city": "",
    "state": "",

    "expiry_id": "",
    "blood_group": "",
    "component": "",
    "expired_units": 0,
    "expiry_date": ""
}


# Alert Event
ALERT_SCHEMA = {
    "event_id": "",
    "event_type": "alert",
    "timestamp": "",
    "blood_bank": "",
    "city": "",
    "state": "",

    "alert_id": "",
    "alert_level": "",
    "message": ""
}