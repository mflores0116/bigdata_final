-- Verify the number of customer records loaded into Hive

SELECT COUNT(*) AS total_customers
FROM customer_churn;

-- Preview records from the managed Hive table

SELECT *
FROM customer_churn
LIMIT 10;

-- Compare churned and non-churned customer counts

SELECT
    target_churn,
    COUNT(*) AS customer_count
FROM customer_churn
GROUP BY target_churn;

-- Compare average spending and satisfaction by churn status

SELECT
    target_churn,
    ROUND(AVG(total_spend), 2) AS avg_total_spend,
    ROUND(AVG(satisfaction_score), 2) AS avg_satisfaction_score
FROM customer_churn
GROUP BY target_churn;
