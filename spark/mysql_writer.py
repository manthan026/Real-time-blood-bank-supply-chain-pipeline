from config import (
    MYSQL_URL,
    MYSQL_TABLE,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_DRIVER,
)


def write_to_mysql(batch_df, batch_id):
    """
    Writes each Spark micro-batch into Amazon RDS MySQL.
    """

   
    print(f"Processing Batch: {batch_id}")
        
    batch_df = batch_df.cache()

    # Count rows
    rows = batch_df.count()
    print(f"Rows in Batch: {rows}")

    if rows == 0:
        print("Empty batch. Skipping...")
        batch_df.unpersist()
        return

    print("\nRecords to be written to Amazon RDS:\n")

    records = batch_df.collect()

    for i, row in enumerate(records, start=1):
        
        print(f"Record #{i}")
        
        print(f"Event ID        : {row.event_id}")
        print(f"Event Type      : {row.event_type}")
        print(f"Blood Group     : {row.blood_group}")
        print(f"Units           : {row.units}")
        print(f"Available Units : {row.available_units}")
        print(f"Blood Bank      : {row.blood_bank}")
        print(f"Hospital        : {row.hospital}")
        print(f"City            : {row.city}")
        print(f"State           : {row.state}")
        print(f"Status          : {row.status}")

    
    print("MySQL Configuration")
    
    print(f"URL   : {MYSQL_URL}")
    print(f"Table : {MYSQL_TABLE}")
    print(f"User  : {MYSQL_USER}")

    try:
        print("\nWriting records to Amazon RDS MySQL...\n")

        (
            batch_df.write
            .format("jdbc")
            .option("url", MYSQL_URL)
            .option("driver", MYSQL_DRIVER)
            .option("dbtable", MYSQL_TABLE)
            .option("user", MYSQL_USER)
            .option("password", MYSQL_PASSWORD)
            .option("batchsize", "500")
            .option("numPartitions", "1") 
            .option("connectTimeout", "10000")
            .option("socketTimeout", "30000")
            .mode("append")
            .save()
)
             
                  
        print(f"Batch {batch_id} written successfully to Amazon RDS!")
        print(f"Total Records Inserted : {rows}")
        

    except Exception as e:
        print("\nERROR WRITING TO AMAZON RDS")
        print(type(e).__name__)
        print(e)
        raise

    finally:
        batch_df.unpersist()