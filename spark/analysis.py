from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import (
    BinaryClassificationEvaluator,
    MulticlassClassificationEvaluator
)
import happybase

# Step 1: Create a Spark session
spark = SparkSession.builder.appName("Customer Churn Prediction").enableHiveSupport().getOrCreate()

# Step 2: Load the data from the Hive table 'customer_churn' into a Spark DataFrame
churn_df = spark.sql("""
    SELECT
        age,
        annual_income,
        total_spend,
        years_as_customer,
        num_of_purchases,
        average_transaction_amount,
        num_of_returns,
        num_of_support_contacts,
        satisfaction_score,
        last_purchase_days_ago,
        target_churn
    FROM customer_churn
""")

# Step 3: Handle null values by either dropping or filling them
churn_df = churn_df.na.drop()  # Drop rows with null values

# Convert churn TRUE/FALSE to numeric label 1/0
churn_df = churn_df.withColumn(
    "label",
    col("target_churn").cast("double")
)

# Step 4: Prepare the data for MLlib by assembling features into a vector
assembler = VectorAssembler(
    inputCols=[
        "age",
        "annual_income",
        "total_spend",
        "years_as_customer",
        "num_of_purchases",
        "average_transaction_amount",
        "num_of_returns",
        "num_of_support_contacts",
        "satisfaction_score",
        "last_purchase_days_ago"
    ],
    outputCol="features",
    handleInvalid="skip"
)

assembled_df = assembler.transform(churn_df).select("features", "label")

# Step 5: Split the data into training and testing sets
train_data, test_data = assembled_df.randomSplit([0.7, 0.3], seed = 1)

# Step 6: Initialize and train a Logistic Regression model
lr = LogisticRegression(featuresCol = "features", labelCol="label")
lr_model = lr.fit(train_data)

# Step 7: Evaluate the model on the test data
test_results = lr_model.evaluate(test_data)

# Step 8: Print the model performance metrics
print(f"Accuracy: {test_results.accuracy}")
print(f"AUC: {test_results.areaUnderROC}")

# ---- Write metrics to HBase with happybase (using the provided pattern) ----
# Example data (row_key, column_family:column, value) populated with the metrics
data = [
    ('metrics1', 'cf:accuracy', str(test_results.accuracy)),
    ('metrics1', 'cf:auc',   str(test_results.areaUnderROC)),
]

# Function to write data to HBase inside each partition
def write_to_hbase_partition(partition):
    connection = happybase.Connection('master')
    connection.open()
    table = connection.table('churn_metrics')  # Update table name
    for row in partition:
        row_key, column, value = row
        table.put(row_key, {column: value})
    connection.close()

# Parallelize data and apply the function with foreachPartition
rdd = spark.sparkContext.parallelize(data)
rdd.foreachPartition(write_to_hbase_partition)

# Step 9: Stop the Spark session
spark.stop()


