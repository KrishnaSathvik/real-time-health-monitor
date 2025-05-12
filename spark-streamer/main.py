from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType
from pyspark.sql.functions import from_json, col

mongo_uri = "mongodb://localhost:27017"
mongo_db = "healthcare"
mongo_collection = "vitals"

spark = SparkSession.builder \
    .appName("RealTimeHealthMonitor") \
    .config("spark.mongodb.output.uri", f"{mongo_uri}/{mongo_db}.{mongo_collection}") \
    .getOrCreate()

schema = StructType([
    StructField("patient_id", IntegerType()),
    StructField("heart_rate", IntegerType()),
    StructField("blood_pressure", StringType()),
    StructField("spo2", IntegerType()),
    StructField("timestamp", DoubleType())
])

raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "health-vitals") \
    .option("startingOffsets", "latest") \
    .load()

parsed_df = raw_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

def write_to_mongo(batch_df, batch_id):
    print(f"\n💾 Writing batch {batch_id}")
    batch_df.printSchema()
    batch_df.show(truncate=False)

    batch_df.select(
        col("patient_id").cast("int"),
        col("heart_rate").cast("int"),
        col("blood_pressure").cast("string"),
        col("spo2").cast("int"),
        col("timestamp").cast("double")
    ).write \
    .format("mongo") \
    .mode("append") \
    .option("uri", f"{mongo_uri}/{mongo_db}.{mongo_collection}") \
    .save()

query = parsed_df.writeStream \
    .foreachBatch(write_to_mongo) \
    .outputMode("append") \
    .option("checkpointLocation", "spark-streamer/checkpoints") \
    .start()

query.awaitTermination()
