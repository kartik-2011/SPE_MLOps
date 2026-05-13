# House Price Prediction MLOps Project

This repository contains a production-style MLOps project for house price prediction.

## Current Status
- Core ML training pipeline implemented
- FastAPI inference service implemented
- Next step: DevOps automation layers

## Planned Components
- ML training pipeline
- FastAPI inference service
- Model versioning
- Automated tests
- Docker and Docker Compose
- Kubernetes deployment
- Jenkins CI/CD
- Ansible automation
- ELK logging

## Quick Start
1. Create a virtual environment and install dependencies:
   `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
2. Train the baseline model:
   `python -m training.train`
3. Run the API:
   `uvicorn app.main:app --reload`
4. Open:
   `http://127.0.0.1:8000/`
5. API docs:
   `http://127.0.0.1:8000/docs`

## Key Commands
- Train using sklearn dataset:
  `python -m training.train --data-source sklearn`
- Train using offline demo dataset:
  `python -m training.train --data-source demo`
- Retrain from a repository CSV:
  `python -m training.retrain --data-source csv --csv-path data/incoming/housing.csv`
- Run tests:
  `pytest`
- Open the web UI:
  `http://127.0.0.1:8000/`
- Start the local app + ELK stack:
  `docker compose up --build`

## CI/CD Flow
1. Push code or new CSV data to GitHub.
2. GitHub webhook triggers Jenkins.
3. Jenkins runs tests and retraining.
4. Jenkins builds and pushes the Docker image.
5. Jenkins deploys the latest image to Kubernetes.
6. Kubernetes updates the running API.
7. Logs appear in Kibana through the ELK pipeline.
