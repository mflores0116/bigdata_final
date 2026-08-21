# Apache NiFi — Data Ingestion into HDFS

## Role in the Pipeline

Apache NiFi provides the ingestion and orchestration layer for this project. The completed flow retrieves the project dataset and writes it into HDFS for downstream processing.

## Source Dataset

**Dataset:** customer_churn.csv 

**GitHub direct URL:** https://raw.githubusercontent.com/mflores0116/predicting_churn_pipeline/refs/heads/main/sample-data/customer_churn.csv

This dataset contains 1,000 online customer retail records. It includes information about customer demographics, purchasing behavior, satisfaction, and marketing engagement. The variable of interest here is customer churn, which reflects how the customer interacts with the company. I selected this dataset because I wanted to explore consumer behavior and determine whether customer characteristics and activity could be used to predict churn. The dataset is already cleaned, which allows the focus of the project to be on building and demonstrating a working pipeline.

## Flow Design

The NiFi flow uses three processors to download the dataset, assign the correct file name, and write the file into HDFS. 

| Processor (Process Group) | Role in the Flow |
|---|---|
| Download File (InvokeHTTP) | Sends an HTTP GET request to download the `customer_churn.csv` into the NiFi flow |
| Update File Name (UpdateAttribute) | Updates the FlowFile `filename` attribute so the downloaded file has the correct project filename |
| Write File into HDFS (PutHDFS)| Writes the completed FlowFile into HDFS directory so it can be accessed by the next part of the pipeline|

The flow begins with the Download File processor, which retrieves `customer_churn.csv` from the GitHub URL. This downloaded data is placed into a FlowFile and passed to the Update File Name processor. This processor sets the filename to `customer_churn.csv`. 

Then, the FlowFile is passed to the Write File to HDFS processor, which connects and writes the dataset to HDFS.

## HDFS Destination

**HDFS Directory:** `/tmp`

**Dataset Path:** `/tmp/customer_churn.csv`

NiFi writes `customer_churn.csv` to the `/tmp` HDFS directory using the PutHDFS processor. This makes the dataset available for the Hive stage of the pipeline.

## Execution Evidence

### Final NiFi Flow

The completed NiFi flow was exported and saved in the repository as:

[`flow-definition.json`](flow-definition.json)

This file contains the configuration for the completed NiFi ingestion flow. 


![NiFi Flow](screenshots/nifi-flow.png)

The completed flow shows the three processors connected in sequence from the Download File processor to the HDFS write operation.

### Running Flow / Queue Activity

![NiFi Running](screenshots/nifi-running.png)

After the `Download File` processor retrieved the dataset, the `Response` queue contains one FlowFile with a size of approximately 69.96 KB. This confirms that `customer_churn.csv` was successfully downloaded from GitHub and is ready to move to the `Update File Name` processor.

![NiFi Running](screenshots/nifi-running2.png)

After passing through the `Update File Name` processor, the 69.96 KB FlowFile was transferred to the `success` queue before being passed to to the `Write File to HDFS` processor. This shows that the dataset successfully moved through the NiFi ingestion flow toward HDFS.

### HDFS Ingestion Verification

![HDFS Verification](screenshots/hdfs-ingestion-verification.png)

Running `hdfs dfs -ls /tmp` confirms that `customer_churn` was successfully written to the `/tmp` directory in HDFS. This verifies that the NiFi ingestion process was successfully completed and the dataset is available for the next stage of the pipeline. 
