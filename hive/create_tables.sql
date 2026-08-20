-- Create a managed Hive table for the online retail customer churn dataset

CREATE TABLE customer_churn (
    customer_id INT,
    age INT,
    gender STRING,
    annual_income DOUBLE,
    total_spend DOUBLE,
    years_as_customer INT,
    num_of_purchases INT,
    average_transaction_amount DOUBLE,
    num_of_returns INT,
    num_of_support_contacts INT,
    satisfaction_score INT,
    last_purchase_days_ago INT,
    email_opt_in BOOLEAN,
    promotion_response STRING,
    target_churn BOOLEAN
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");

-- Load the customer churn dataset from HDFS into the managed Hive table

LOAD DATA INPATH '/tmp/customer_churn.csv'
INTO TABLE customer_churn;
