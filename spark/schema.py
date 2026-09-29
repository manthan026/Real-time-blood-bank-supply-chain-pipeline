from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType
)

blood_bank_schema = StructType([

    StructField("event_id", StringType(), True),
    StructField("timestamp", StringType(), True),

    StructField("blood_bank", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),

    StructField("event_type", StringType(), True),

    StructField("donor_id", StringType(), True),
    StructField("donor_name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("gender", StringType(), True),

    StructField("blood_group", StringType(), True),
    StructField("component", StringType(), True),

    StructField("units", IntegerType(), True),
    StructField("status", StringType(), True),

    StructField("request_id", StringType(), True),
    StructField("hospital", StringType(), True),
    StructField("priority", StringType(), True),

    StructField("screening_id", StringType(), True),
    StructField("screening_status", StringType(), True),

    StructField("transfer_id", StringType(), True),
    StructField("destination_bank", StringType(), True),

    StructField("dispatch_id", StringType(), True),

    StructField("inventory_id", StringType(), True),
    StructField("available_units", IntegerType(), True),

    StructField("expiry_id", StringType(), True),
    StructField("expired_units", IntegerType(), True),
    StructField("expiry_date", StringType(), True),

    StructField("alert_id", StringType(), True),
    StructField("alert_level", StringType(), True),
    StructField("message", StringType(), True)
])