from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json

from config import (
    APP_NAME,
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC,
    CHECKPOINT_LOCATION,
    MYSQL_JAR_PATH
)

from schema import blood_bank_schema
from transformations import transform_data
from mysql_writer import write_to_mysql


def create_spark_session():
    """
    Creates and returns a Spark Session.
    """

    print("\n========== Creating Spark Session ==========\n")

    spark = (
        SparkSession.builder
        .appName(APP_NAME)
        .master("local[*]")

       

        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    print("Spark Session Created Successfully")
    print("Application Name :", APP_NAME)
    print("Kafka Topic      :", KAFKA_TOPIC)
    print("Checkpoint Path  :", CHECKPOINT_LOCATION)

    return spark


if __name__ == "__main__":

    try:

        
        # Create Spark Session
       
        spark = create_spark_session()

        print("\n========== Reading Kafka Stream ==========\n")

        kafka_df = (
            spark.readStream
            .format("kafka")
            .option(
                "kafka.bootstrap.servers",
                KAFKA_BOOTSTRAP_SERVERS
            )
            .option(
                "subscribe",
                KAFKA_TOPIC
            ).option("failOnDataLoss", "false")
            .option(
                "startingOffsets",
                "latest"
            )
            .load()
        )

       
        # Convert Binary -> String
        

        json_df = (
            kafka_df.selectExpr(
                "CAST(value AS STRING) AS json_data"
            )
        )

       
        # Parse JSON
       

        parsed_df = (
            json_df
            .select(
                from_json(
                    col("json_data"),
                    blood_bank_schema
                ).alias("data")
            )
            .select("data.*")
        )

       
        # Transform Data
       

        transformed_df = transform_data(parsed_df)

        print(" Data Transformation Pipeline Ready")

       
        # Write to Amazon RDS
        

        query = (
            transformed_df.writeStream
            .foreachBatch(write_to_mysql)
            .outputMode("append")
            .option(
                "checkpointLocation",
                CHECKPOINT_LOCATION
            )
            .start()
        )

        
        print(" Blood Bank Streaming Started")
       
        print(f"Kafka Topic     : {KAFKA_TOPIC}")
        print(f"Checkpoint Path : {CHECKPOINT_LOCATION}")
        print("Waiting for incoming records...\n")

        query.awaitTermination()

    except KeyboardInterrupt:
        print("\n Streaming stopped by user.")

    except Exception as e:
        print("\n STREAMING FAILED")
        print(type(e).__name__)
        print(e)
        raise

    finally:
        print("\nStopping Spark Session...")
        spark.stop()
        print("Spark Session Stopped")
