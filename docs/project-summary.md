# Project Summary

## Implementation Overview

Summarize the end-to-end project in your own words.

Describe the dataset, the purpose of the pipeline, and how the major technologies work together:

**Source Data → NiFi → HDFS → Hive → Spark MLlib → HBase**

Spark execution is submitted through **YARN**.

## Dataset

**Dataset name:** [Enter dataset name]  
**GitHub direct URL:** [Enter direct/raw dataset URL]

Briefly explain what the dataset contains and why it is appropriate for the selected Spark MLlib workflow.

## Environment Setup

Before running the Spark MLlib application, the Python environment was prepared on the master and worker containers by installing the `numpy` and `happybase` packages.

These packages were installed using:

```bash
pip3 install numpy happybase
```

The HappyBase Python library is required because PySpark uses it to connect to HBase and write the final model-performance metrics. NumPy was installed for numerical and data-processing capabilities.

Both packages were installed on the master, worker1, and worker2 containers so the Python dependencies are available across the Spark environment.

### Package Installation Evidence

![Package Installation](screenshots/package-installation.png)

The package installation completed successfully, confirming that the Python environment is ready for the Spark-to-HBase part of the pipeline.

### HBase Thrift Server Evidence

The HBase Thrift server was started on the master container before running the Spark application.

The Thrift server provides the connection between the `happybase` library and HBase. This service is needed so that PySpark can write the accuracy and AUC values into the `churn_metrics` table. 

The service was started using:

```bash
nohup hbase thrift start &
```

![HBase Thrift Server](screenshots/hbase-thrift-server.png)

The running HBase Thrift process confirms that the service is available before running the Spark MLlib application.

## What Worked

Summarize the major portions of the pipeline that executed successfully.

## Issues & Challenges Encountered

Describe the most meaningful technical problems encountered while building the project.

For each important challenge, explain:

1. what happened;
2. how you investigated it;
3. what you changed or fixed;
4. what you learned from the issue.

## Results

Summarize the final technical results, including the successful movement of data through the pipeline and the machine learning results produced by Spark MLlib.

## Lessons Learned

Describe the most important technical lessons gained from integrating multiple distributed services in one environment.

## Production Considerations

Explain what you would change if this architecture were being deployed as a production system.

Possible areas to consider include:

- security and authentication;
- high availability;
- observability and monitoring;
- resource sizing;
- automation and CI/CD;
- data governance;
- secrets management;
- scalability and fault tolerance.
