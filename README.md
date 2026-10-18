# Containerized Real-Time Credit Card Fraud Detection Microservice

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688?logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)

An enterprise-ready, containerized RESTful API microservice that predicts credit card fraud in real time using a Scikit-Learn Machine Learning pipeline, FastAPI, OAuth2 JWT authentication, and Docker.

---

## Key System Architecture Features

* **High-Performance Inference:** Sub-20ms model prediction endpoint powered by FastAPI and Uvicorn.
* **Robust Security:** OAuth2 authentication scheme with signed JWT bearer tokens and password hashing.
* **Containerized Deployment:** Lightweight Docker container using a hardened non-root user environment with integrated container health checks.
* **Model Pipeline:** Scikit-Learn pipeline (`StandardScaler` + `LogisticRegression`) handling severe class imbalance with custom probability thresholds.
* **Automated CI/CD:** GitHub Actions pipeline executing unit tests (`pytest`) and automatically building/publishing Docker images to Docker Hub.

---

## Tech Stack

* **Core Framework:** Python 3.11, FastAPI, Pydantic v2
* **Machine Learning:** Scikit-learn, Pandas, NumPy, Joblib
* **Security & Auth:** PyJWT, Passlib, OAuth2
* **Containerization & DevOps:** Docker, WSL 2, GitHub Actions CI/CD
* **Testing:** Pytest, HTTPX

---

## Quick Start (Docker)

### 1. Pull and Run from Docker Hub
```bash
docker run -d -p 8000:8000 --name fraud_api your-dockerhub-username/fraud-detection-api:latest