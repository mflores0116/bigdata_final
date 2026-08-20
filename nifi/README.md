# Apache NiFi — Data Ingestion into HDFS

## Role in the Pipeline

Apache NiFi provides the ingestion and orchestration layer for this project. The completed flow retrieves the project dataset and writes it into HDFS for downstream processing.

## Source Dataset

**Dataset:** customer_churn.csv 
**GitHub direct URL:** https://raw.githubusercontent.com/mflores0116/bigdata_final/refs/heads/main/sample-data/customer_churn.csv

This dataset contains 1000 customer records. 

## Flow Design

The NiFi flow uses three processors to download the dataset, assign the correct file name, and write the file into HDFS. 
Describe the important processors used in the final NiFi flow and the role each processor performs.

| Processor / Process Group | Role in the Flow |
|---|---|
| Download File (InvokeHTTP) | Sends an HTTP Get request to download the customer_churn.csv into the Nifi flow |
| Update File Name (UpdateAttribute) | Updates the FlowFile 'filename' attribute so the downloaded file has the correct project filename |
| Write File into HDFS (PutHDFS)| Writes the completed FlowFile into HDFS directory so it can be accessed by the next part of the pipeline|

Explain how data moves from the source URL through NiFi and into HDFS.

## HDFS Destination

**HDFS path:** `[Enter final HDFS path]`

Explain where NiFi writes the dataset and how the destination is used by the next stage of the pipeline.

## Execution Evidence

### Final NiFi Flow

![NiFi Flow](C:\Users\mirey\Documents\Bellevue\Big Data\Week 11)

### Running Flow / Queue Activity

![NiFi Running] <img width="343" height="286" alt="image" src="https://github.com/user-attachments/assets/344e8c91-426c-46e2-949a-a6c9256d48ef" />


### HDFS Ingestion Verification

![HDFS Verification](screenshots/hdfs-ingestion-verification.png)

The HDFS screenshot should show the `hdfs dfs -ls` output confirming that the project dataset was successfully written into HDFS.
