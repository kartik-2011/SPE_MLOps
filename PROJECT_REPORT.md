# Automated MLOps Pipeline for Continuous Model Training and Deployment

## Abstract
This project presents a production-oriented MLOps system for house price prediction. The goal is to move beyond a simple machine learning model and build a complete automated pipeline that supports model training, testing, versioning, containerization, deployment, monitoring, and continuous updates. The system uses a house price prediction model as the application domain and integrates DevOps tools such as GitHub, Jenkins, Docker, Docker Compose, Kubernetes, Ansible, and the ELK stack. When new code or data is pushed to the repository, the pipeline retrains the model, runs tests, builds and pushes Docker images, deploys the updated application, and makes logs available in Kibana for monitoring and analysis.

## 1. Introduction
Modern software systems require more than just correct functionality. They must also support automation, scalability, continuous delivery, and monitoring. Machine learning applications add another layer of complexity because they involve data, training workflows, model versioning, and ongoing retraining.

This project combines machine learning with DevOps practices to create a self-updating house price prediction system. Instead of treating the machine learning model as a one-time artifact, the project manages it through an end-to-end lifecycle. The final system demonstrates how new data or code changes can automatically trigger retraining and redeployment in a production-style environment.

## 2. Problem Statement
Traditional academic machine learning projects often focus only on training a model and showing prediction results. However, real-world machine learning systems must handle:

- repeated training with updated data
- model version control
- automated testing
- containerized deployment
- scalable orchestration
- centralized logging and monitoring

The problem addressed in this project is how to design and implement a complete MLOps pipeline that automates these tasks while using a practical machine learning use case, namely house price prediction.

## 3. Project Objective
The main objective of the project is to build an automated MLOps pipeline for continuous model training and deployment. The system should:

- train a house price prediction model
- expose the model through an API
- retrain the model when new data is available
- automatically test and package the application
- deploy the updated application using containers and Kubernetes
- collect logs and visualize them through the ELK stack

## 4. Domain and Use Case
The selected domain for this project is MLOps. The application use case is house price prediction using a regression model. This domain is suitable because it clearly demonstrates the full lifecycle of a machine learning system, from training and inference to redeployment and observability.

The project is not focused on building the most advanced prediction model. Instead, it emphasizes reliable automation, reproducibility, and operational readiness.

## 5. Dataset and Model Selection
The first version of the system uses the California Housing dataset available through `scikit-learn` with `fetch_california_housing()`. This dataset is chosen because:

- it is easy to access and consistent
- it removes dependency on external APIs or manual downloads
- it contains structured numerical features suitable for regression
- it allows rapid creation of a working baseline model

The initial model will be trained using a regression algorithm such as `RandomForestRegressor`. The trained model will be stored as a versioned artifact, for example `model_v1.pkl`, and accompanied by metadata including evaluation metrics and timestamps.

In later stages, the system will also support retraining from locally pushed CSV files so that new datasets added to the repository can trigger an updated training cycle.

## 6. Proposed System Architecture
The system consists of the following major components:

- Training pipeline for model building and evaluation
- Model registry for storing versioned models and metadata
- FastAPI-based inference service for prediction requests
- Jenkins CI/CD pipeline for automation
- Docker and Docker Compose for containerization
- Kubernetes for orchestration and scaling
- Ansible for automated setup and deployment tasks
- ELK stack for logging and monitoring

### High-Level Workflow
1. The model is trained using the available dataset.
2. The trained model is saved along with version and performance metadata.
3. A FastAPI service loads the current production model and serves predictions.
4. Changes pushed to GitHub trigger the Jenkins pipeline.
5. Jenkins runs tests, retrains the model if required, builds a Docker image, and pushes it to Docker Hub.
6. Kubernetes deploys the latest application image.
7. Application logs are forwarded to the ELK stack and visualized in Kibana.

## 7. Tools and Technologies
The project uses the following tools:

- `Python` for machine learning and backend logic
- `scikit-learn` for dataset access, training, and evaluation
- `FastAPI` for exposing prediction endpoints
- `Git` and `GitHub` for version control
- `Jenkins` for CI/CD pipeline automation
- `Docker` for containerization
- `Docker Compose` for local multi-service execution
- `Kubernetes` for deployment and scaling
- `Ansible` for configuration management and automation
- `ELK Stack` for centralized logging and visualization

## 8. Project Modules

### 8.1 Training Module
This module is responsible for:

- loading data
- preprocessing and splitting datasets
- training the regression model
- evaluating the model using metrics such as MAE, RMSE, and R2
- saving the trained model with version information

### 8.2 Inference Module
This module provides a REST API to users. It is responsible for:

- loading the active production model
- accepting prediction requests
- returning house price predictions
- exposing health and model information endpoints

### 8.3 Model Versioning Module
This module manages:

- model artifacts
- model metadata
- currently active production model
- comparison of candidate and deployed model versions

### 8.4 CI/CD Module
The CI/CD module uses Jenkins to:

- fetch the latest code from GitHub
- run automated tests
- retrain the model if new data is present
- build Docker images
- push images to Docker Hub
- deploy the application to Kubernetes

### 8.5 Deployment Module
This module includes Docker, Docker Compose, Kubernetes, and Ansible configurations used to package, deploy, and scale the application.

### 8.6 Logging and Monitoring Module
This module collects application logs and forwards them to Elasticsearch through Logstash or Filebeat. Kibana dashboards are then used to visualize prediction activity, model version usage, and system events.

## 9. CI/CD Pipeline Flow
The CI/CD pipeline is the core of the project. Its expected flow is:

1. Developer pushes code or new data to GitHub.
2. GitHub webhook triggers Jenkins.
3. Jenkins checks out the latest repository.
4. Automated tests are executed.
5. The training pipeline builds a candidate model.
6. If the candidate model performs better, it is promoted as the new model version.
7. A new Docker image is built and tagged.
8. The image is pushed to Docker Hub.
9. Kubernetes updates the deployment with the latest image.
10. The updated API becomes available with minimal disruption.

This satisfies the project requirement that incremental repository updates should trigger automated build, test, containerization, and deployment workflows.

## 10. Logging and ELK Integration
To satisfy the monitoring requirement, the application will generate structured logs for:

- incoming prediction requests
- model versions used for predictions
- training and deployment events
- errors and exceptions
- health check requests

These logs will be collected and sent to the ELK stack:

- `Elasticsearch` stores the log data
- `Logstash` or `Filebeat` processes and forwards logs
- `Kibana` provides dashboards and search capabilities

This allows the project to demonstrate observability and operational monitoring in a production-like setup.

## 11. Security and Advanced Features
The project will also attempt to include advanced features encouraged in the project guidelines:

- Kubernetes Secrets for sensitive configuration
- Ansible roles for modular automation
- Horizontal Pod Autoscaling in Kubernetes for scalability
- rolling updates for near zero-downtime deployment

If feasible, secure credential storage using Vault may also be considered.

## 12. Expected Outcomes
At the end of the project, the following outcomes are expected:

- a working house price prediction API
- automated retraining workflow
- model version tracking
- Dockerized services
- Kubernetes-based deployment
- Jenkins-driven CI/CD automation
- centralized logging with Kibana dashboards

The final result will be a practical demonstration of how DevOps practices can be applied to machine learning systems in a real-world production style.

## 13. Demo Strategy
The project demonstration will follow these steps:

1. Show the running prediction API and generate a prediction.
2. Add or modify data and push changes to GitHub.
3. Show Jenkins automatically triggering the pipeline.
4. Show tests, retraining, image build, and deployment stages.
5. Refresh the deployed application and show the updated version.
6. Open Kibana and show application logs and model-related events.

This clearly demonstrates continuous integration, continuous deployment, automated retraining, and monitoring in one end-to-end flow.

## 14. Conclusion
This project demonstrates how machine learning can be integrated into a modern DevOps workflow through MLOps principles. Rather than stopping at model training, it covers the entire operational lifecycle of the application, including testing, deployment, scaling, and monitoring. By using a house price prediction system as the application domain, the project provides a practical and understandable example of continuous model training and deployment in a production-style environment.
