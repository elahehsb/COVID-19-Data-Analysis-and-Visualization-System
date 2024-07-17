from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType

def main():
    spark = SparkSession.builder \
        .appName("COVID Analysis") \
        .getOrCreate()

    schema = StructType([
        StructField("Country", StringType(), True),
        StructField("TotalConfirmed", IntegerType(), True),
        StructField("TotalDeaths", IntegerType(), True),
        StructField("TotalRecovered", IntegerType(), True),
        StructField("Date", StringType(), True)
    ])

    kafka_df = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "covid") \
        .load()

    covid_df = kafka_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")

    query = covid_df.writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()
