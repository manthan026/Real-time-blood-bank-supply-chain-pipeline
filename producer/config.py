#Real time blood bank and supply chain pipeline

# Kafka broker address where the producer sends messages.
KAFKA_BROKER = "localhost:9092"

# Single Kafka topic that stores all blood bank events.
TOPIC_NAME = "blood-bank-events"

# Unique identifier for this Kafka producer.
PRODUCER_CLIENT_ID = "blood-bank-producer"

# Time interval (in seconds) between generating two events.
MESSAGE_INTERVAL = 2


# Different types of events generated in the blood bank system.
EVENT_TYPES = [
    "donation",
    "request",
    "screening",
    "transfer",
    "dispatch",
    "inventory",
    "expiry",
    "alert"
]


# Supported blood groups.
BLOOD_GROUPS = [
    "A+",
    "A-",
    "B+",
    "B-",
    "AB+",
    "AB-",
    "O+",
    "O-"
]


# Blood banks participating in the supply chain.
BLOOD_BANKS = [
    "AIIMS Blood Bank",
    "Safdarjung Blood Bank",
    "Apollo Blood Centre",
    "Fortis Blood Bank",
    "Max Hospital Blood Bank",
    "BLK Blood Centre",
    "RML Blood Bank",
    "GTB Blood Centre"
]


# Hospitals that can request or receive blood units.
HOSPITALS = [
    "AIIMS Delhi",
    "Safdarjung Hospital",
    "Apollo Hospital",
    "Fortis Hospital",
    "Max Hospital",
    "BLK Hospital",
    "RML Hospital",
    "GTB Hospital"
]


# Cities where blood banks and hospitals are located.
CITIES = [
    "Delhi",
    "Noida",
    "Gurugram",
    "Faridabad",
    "Ghaziabad"
]


# State of operation.
STATE = "Delhi NCR"


# Blood components available after blood separation.
COMPONENTS = [
    "Whole Blood",
    "Plasma",
    "Platelets",
    "Red Cells",
    "Cryoprecipitate"
]


# Inventory status used by the dashboard and alerts.
INVENTORY_STATUS = [
    "Available",
    "Low Stock",
    "Critical",
    "Out of Stock"
]


# Possible screening outcomes after laboratory testing.
SCREENING_STATUS = [
    "Passed",
    "Rejected",
    "Pending"
]


# Current dispatch status of blood units.
DISPATCH_STATUS = [
    "Packed",
    "Dispatched",
    "Delivered"
]


# Severity level of system alerts.
ALERT_LEVELS = [
    "INFO",
    "WARNING",
    "CRITICAL"
]


# Current status of blood transfer between blood banks.
TRANSFER_STATUS = [
    "Initiated",
    "In Transit",
    "Completed"
]