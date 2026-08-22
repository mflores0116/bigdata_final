# Interview Talking Points

Use this file to prepare a concise explanation of the project for a technical interview.

## 30-Second Overview

> I built an end-to-end distributed data pipeline using Apache NiFi, HDFS, Hive, Spark MLlib, YARN, and HBase. The project used a customer churn dataset with 1,000 records. NiFi ingested the source dataset from GitHub and wrote it into HDFS, and Hive loaded the data into a managed table for SQL access. Spark MLlib read the Hive data then used logistic regression to predict customer churn, with YARN managing the Spark workload. The final accuracy and AUC results were written into HBase to complete the pipeline. This repository preserves the architecture, code, and execution evidence so the implementation can be reviewed without a live cloud environment.

## Be Ready to Explain

### What problem or analytical task did your dataset support?

The dataset supports a customer churn prediction task. The goal is to use customer demographics, purchasing behavior, satisfaction levels, and marketing responses to predict whether a customer churns.

### Walk through the complete data flow.

The dataset is stored in GitHub as `customer_churn.csv`. Nifi downloads the file then writes it into HDFS. Then, Hive loads the data into the `customer_churn` managed table. Spark reads the table from Hive, prepares the data, and trains a logistic regression model using MLlib. The Spark application runs through YARN and then final accuracy and AUC are written into the `churn_metrics` HBase table.

### Why did you use NiFi?

NiFi is used as the ingestion layer because it provides a way to retrieve the data from GitHub and move it into HDFS. The flow also gives a way to visually track the file as it moves through each processor.

### What role did HDFS play?

HDFS provides distributed storage for the dataset after NiFi downloads it. The files is stored at `/tmp/customer_churn.csv` and is used as the source for loading the Hive table.

### How did you design the Hive table?

The Hive table is called `customer_churn` and contains 15 columns that match the structure of the original CSV file. Numeric fields use numeric data types, categorical fields are stored as strings, and `email_opt_in` and `target_churn` are stored as Boolean variables. The header row is skipped during the initial data loading. 

### What data did Spark read from Hive?

Spark reads the numeric fields from the `customer_churn` Hive table. These columns are age, annual income, total spend, years as customer, number of purchases, average transaction amount, returns, support contacts, satisfaction score, and days since last purchase. The model label is `target_churn` and is the field the model will try to predict. 

### Which MLlib algorithm did you use and why?

I used a logistic regression because the target variable is binary. A customer either churns or does not churn, so logistic regression is an appropriate classification model for the tasks.

### How did you evaluate the model?

To evaluate the model, I split the original data using a 70/30 split with a random seed of 1. This means that 70% of the model serves as training data and the remaining 30% is the testing data. The model accuracy is evaluated by calculating the accuracy and area under the ROC curve (AUC). The model gave an accuracy of 0.49 and AUC of approximately 0.44. 

### What did YARN do during Spark execution?

YARN is a resource manager that manages the Spark workload and allows Spark tasks to run across multiple worker nodes. I submitted the PySpark application using `spark-submit` with YARN as the master.

### Why did you write model metrics into HBase?

I used HBase to store the final results from the Spark model. After Spark calculated the accuracy and AUC, those metrics are written into the `churn_metrics` table so they can be saved and reviewed even after the Spark job is complete.

### How did the final HBase scan prove the pipeline worked?

When the HBase table was first created, it was scanned and returned `0 row(s)`. After the Spark application finishes, it writes the metrics to the HBase table under the `metrics1` row key. The final scan confirms that Spark generated the correct metrics and successfully wrote them into HBase.

### What was the most difficult technical problem?

One of the most difficult parts of this project was getting all the services to work together in the same environment. Each part of the pipeline depends on the other services being ready. For example, the HDFS containers need to be running before NiFi can write the dataset into HDFS.

### How did you troubleshoot it?

To ensure the pipeline is working as expected, I worked through each step and performed some checks along the way. I check that the containers are running in HDFS so that the data can be written into it. The Hive table is tested by executing some SQL queries on it, Spark logs are reviewed to check the MLlib process, and the HBase table is scanned both before and after the Spark job runs. This makes it easy to identify if any parts of the pipeline are not working before moving to the next step. 

### What would you change for production?

For a production environment, I would use a more permanent and secure HDFS storage location instead of `/tmp`. For the machine learning portion, I would include different features, conduct feature engineering, and test different models such as a random forest to see if there is something with more predictive power.
