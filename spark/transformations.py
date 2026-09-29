from pyspark.sql.functions import (
    col,
    upper,
    trim,
    to_timestamp,
    current_timestamp,
    to_date,
    hour,
    when
)


def transform_data(df):
    """
    Cleans and transforms incoming streaming data.
    """

    ts_expr = to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss")

    transformed_df = (
        df
        .withColumns({

            # Clean text fields
            "blood_bank": trim(col("blood_bank")),
            "city": trim(col("city")),
            "hospital": trim(col("hospital")),
            "component": trim(col("component")),

            # Standardize values
            "event_type": upper(col("event_type")),
            "blood_group": upper(col("blood_group")),
            "status": upper(col("status")),

            # Timestamp fields
            "event_timestamp": ts_expr,
            "processed_time": current_timestamp(),
            "event_date": to_date(ts_expr),
            "event_hour": hour(ts_expr),

            # Prevent negative units
            "units": when(
                col("units") < 0,
                0
            ).otherwise(col("units"))
        })

        # Fill numeric NULL values
        .fillna({
            "age": 0,
            "units": 0,
            "available_units": 0,
            "expired_units": 0
        })

        # Fill string NULL values
        .fillna({
            "donor_id": "N/A",
            "donor_name": "N/A",
            "gender": "N/A",
            "blood_group": "N/A",
            "component": "N/A",
            "status": "N/A",
            "request_id": "N/A",
            "hospital": "N/A",
            "priority": "N/A",
            "screening_id": "N/A",
            "screening_status": "N/A",
            "transfer_id": "N/A",
            "destination_bank": "N/A",
            "dispatch_id": "N/A",
            "inventory_id": "N/A",
            "expiry_id": "N/A",
            "expiry_date": "N/A",
            "alert_id": "N/A",
            "alert_level": "N/A",
            "message": "N/A"
        })
    )

    # Set available_units only for INVENTORY events
    transformed_df = transformed_df.withColumn(
        "available_units",
        when(
            col("event_type") == "INVENTORY",
            col("units")
        ).otherwise(col("available_units"))
    )

    return transformed_df