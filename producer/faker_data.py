"""
faker_data.py

Generates fake events for the Blood Bank Supply Chain
Management System using Faker.
"""

import random
import uuid
from datetime import datetime, timedelta
from faker import Faker

from config import (
    BLOOD_BANKS,
    BLOOD_GROUPS,
    HOSPITALS,
    CITIES,
    STATE,
    COMPONENTS,
    SCREENING_STATUS,
    DISPATCH_STATUS,
    ALERT_LEVELS,
    TRANSFER_STATUS
)

# Initialize Faker
fake = Faker("en_IN")


# Generate common fields for every event
def common_event():
    return {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "blood_bank": random.choice(BLOOD_BANKS),
        "city": random.choice(CITIES),
        "state": STATE
    }


# Donation Event
def donation():
    return {
        "donor_id": f"DONOR-{random.randint(10000,99999)}",
        "donor_name": fake.name(),
        "age": random.randint(18, 60),
        "gender": random.choice(["Male", "Female"]),
        "blood_group": random.choice(BLOOD_GROUPS),
        "component": random.choice(COMPONENTS),
        "units": random.randint(1, 5),
        "status": random.choice([
            "Successful",
            "Deferred",
            "Cancelled"
        ])
    }


# Blood Request Event
def request():
    return {
        "request_id": f"REQ-{random.randint(10000,99999)}",
        "hospital": random.choice(HOSPITALS),
        "blood_group": random.choice(BLOOD_GROUPS),
        "component": random.choice(COMPONENTS),
        "units": random.randint(1, 10),
        "priority": random.choice([
            "Low",
            "Medium",
            "High",
            "Critical"
        ]),
        "status": random.choice([
            "Pending",
            "Approved",
            "Completed"
        ])
    }


# Blood Screening Event
def screening():
    return {
        "screening_id": f"SCR-{random.randint(10000,99999)}",
        "blood_group": random.choice(BLOOD_GROUPS),
        "status": random.choice(SCREENING_STATUS),
        "remarks": random.choice([
            "All tests passed",
            "Hemoglobin level low",
            "Blood pressure high",
            "Infectious marker detected",
            "Sample under review"
        ])
    }


# Blood Transfer Event
def transfer():

    source = random.choice(BLOOD_BANKS)
    destination = random.choice(
        [bank for bank in BLOOD_BANKS if bank != source]
    )

    return {
        "transfer_id": f"TRF-{random.randint(10000,99999)}",
        "source_bank": source,
        "destination_bank": destination,
        "blood_group": random.choice(BLOOD_GROUPS),
        "component": random.choice(COMPONENTS),
        "units": random.randint(1, 10),
        "status": random.choice(TRANSFER_STATUS)
    }


# Blood Dispatch Event
def dispatch():
    return {
        "dispatch_id": f"DSP-{random.randint(10000,99999)}",
        "hospital": random.choice(HOSPITALS),
        "blood_group": random.choice(BLOOD_GROUPS),
        "component": random.choice(COMPONENTS),
        "units": random.randint(1, 8),
        "status": random.choice(DISPATCH_STATUS)
    }


# Inventory Event
def inventory():

    units = random.randint(20, 300)

    if units == 0:
        status = "Out of Stock"
    elif units <= 10:
        status = "Critical"
    elif units <= 30:
        status = "Low Stock"
    else:
        status = "Available"

    return {
        "inventory_id": f"INV-{random.randint(10000,99999)}",
        "blood_group": random.choice(BLOOD_GROUPS),
        "component": random.choice(COMPONENTS),
        "units": units,
        "available_units": units,
        "status": status
    }

# Blood Expiry Event
def expiry():
    return {
        "expiry_id": f"EXP-{random.randint(10000,99999)}",
        "blood_group": random.choice(BLOOD_GROUPS),
        "component": random.choice(COMPONENTS),
        "expired_units": random.randint(1, 10),
        "expiry_date": (
            datetime.now() +
            timedelta(days=random.randint(1, 35))
        ).strftime("%Y-%m-%d")
    }


# Alert Event
def alert():
    return {
        "alert_id": f"ALT-{random.randint(10000,99999)}",
        "alert_level": random.choice(ALERT_LEVELS),
        "message": random.choice([
            "Low stock detected",
            "Critical shortage of O- blood",
            "Blood units nearing expiry",
            "Emergency request received",
            "Transfer delayed",
            "Dispatch completed",
            "Inventory updated",
            "Screening failed for donor"
        ])
    }


# Mapping event names to their generator functions
EVENT_GENERATORS = {
    "donation": donation,
    "request": request,
    "screening": screening,
    "transfer": transfer,
    "dispatch": dispatch,
    "inventory": inventory,
    "expiry": expiry,
    "alert": alert
}


# Generate one random event
def generate_event():

    event_type = random.choice(list(EVENT_GENERATORS.keys()))

    event = common_event()

    event["event_type"] = event_type

    event.update(EVENT_GENERATORS[event_type]())

    return event


# Run this file directly to test event generation
#if __name__ == "__main__":

 #   for _ in range(5):
  #      print(generate_event())