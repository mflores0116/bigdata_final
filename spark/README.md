# Apache Spark MLlib — Distributed Machine Learning

## Role in the Pipeline

Apache Spark MLlib provides the distributed processing and machine learning layer for this project. The PySpark application reads project data from Hive, prepares the data for modeling, trains and evaluates a machine learning model, and generates model-performance metrics that are written into HBase.

## Hive Input

**Hive table:** `customer_churn`

Spark reads the customer churn data directly from the managed Hive table created earlier in the pipeline. The machine learning workflow uses numeric customer and purchasing variables as predictors and `target_churn` as the target variable.

The selected input features are:

- age
- annual_income
- total_spend
- years_as_customer
- num_of_purchases
- average_transaction_amount
- num_of_returns
- num_of_support_contacts
- satisfaction_score
- last_purchase_days_ago

The `target_churn` field identifies whether a customer churned and is used as the model label.

## Data Preparation & Transformations

Describe the important preprocessing or transformation steps performed before model training.

Examples may include:

- selecting relevant features;
- handling missing values;
- encoding categorical fields;
- assembling feature vectors;
- scaling or normalization;
- creating training and test datasets.

## MLlib Algorithm

**Algorithm:** Logistic Regression

Logistic regression was chosen because the target variable is binary. Each customer is classified as either churned or not churned, making this a binary classification problem.

The model uses customer demographics, purchasing behavior and satisfaction score to predict `target_churn`. 

## Training & Evaluation

The logistic regression model was trained on 70% of the data and evaluated by predicting the remaining 30%. 

**Primary evaluation metric(s):** Accuracy and Area Under the ROC Curve (AUC)

Explain what the resulting values indicate about model performance.

### Training Output

![Spark Training Output](screenshots/spark-training-output.png)

### Model Evaluation

![Spark ML Evaluation](screenshots/spark-ml-evaluation1.png)
![Spark ML Evaluation](screenshots/spark-ml-evaluation2.png)

## Spark Submit / YARN Execution

The PySpark application was submitted through YARN using:

```bash
spark-submit \
  --master yarn \
  --deploy-mode client \
  --name CustomerChurn_to_HBase \
  analysis.py
```

Briefly describe the successful execution and any important log or output information.

![Spark Submit Output](screenshots/spark-submit-output.png)

## HBase Output

List the model-performance metrics written by Spark into HBase and explain how the application connects the machine learning stage to the final persistence layer.

**PySpark source files:**  [`analysis.py`](analysis.py)
