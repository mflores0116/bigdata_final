# Apache Hive — Managed Table & SQL Validation

## Role in the Pipeline

Apache Hive provides the structured SQL layer between HDFS storage and the Spark MLlib workload. The project data loaded through NiFi into HDFS is used to create and populate a Hive managed table.

## Hive Table Design

**Table name:** `customer_churn`

The `customer_churn` managed table has 15 columns that represent customer demographics, purchasing behavior, satisfaction, marketing engagement, and churn status. 

In this table schema, numeric fields include `age`, `annual_income`, `total_spend`, `years_as_customer`, `num_of_purchases`, `average_transaction_amount`, `num_of_returns`, `num_of_support_contacts`, `satisfaction_score`, and `last_purchase_days_ago`. The categorical fields `gender` and `promotion_response` are stored as strings, while `email_opt_in` and `target_churn` are stored as Boolean values.

The target variable for the Spark MLlib portion of this project is `target_churn`, which identifies whether a customer churned.

The table was created as a managed Hive table using a comma-delimited text format. The header row was skipped so only the customer records were loaded into the table.

## SQL Files

- [`create_tables.sql`](create_tables.sql) — table creation and data-loading SQL
- [`queries.sql`](queries.sql) — validation, exploration, and aggregation queries

## Data Load Verification

The dataset was loaded from `/tmp/customer_churn.csv` in HDFS into the `customer_churn` managed Hive table. 

![Hive Load Results](screenshots/hive-load-results.png)

The data load was verified by displaying records from the table and confirming the values correctly match the Hive schema. 

## Query & Aggregation Verification

A series of queries were run to confirm the table was properly loaded and can be queried using SQL commands.

First, a row-count query was used to confirm that all 1,000 customer records were successfully loaded. 
![Hive Query Results](screenshots/hive-query-results1.png)

The row-count result returned exactly 1,000 records, confirming that all customer data was successfully loaded into the Hive table

Next, a churn aggregation query counted the number of customers in each target class:
  
  - No Churn (false): 474 customers
  - Churn (true): 526 customers
    
![Hive Query Results](screenshots/hive-query-results2.png)

This confirms that all 1,000 customer records are represented in the churn target. Additionally, the two options are relatively well balanced.

Finally, an aggregation query compared average total spending and satisfaction scores by churn status. 

![Hive Query Results](screenshots/hive-query-results3.png)

Customers who did not churn had an average total spend of 4,994.43 and an average satisfaction score of 2.94, while customers who churned had an average total spend of 5,158.62 and an average satisfaction score of 3.00.

This query confirms that the numeric fields were loaded with the correct data types and can be used successfully in Hive aggregation calculations.

The validated Hive table becomes the structured input used by the PySpark MLlib application.
