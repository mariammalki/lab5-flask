#!/bin/bash
# Installation script for lab5-Flask-app

# Variables
IMAGE_NAME="mariem507/flask-app"
TAG="v1"

echo "=== Step 1: Build Docker image ==="
docker build -t lab5-app:latest .

echo "=== Step 2: Push image to DockerHub ==="
docker push mariem507/lab5-app:latest

echo "=== Step 3: Apply Kubernetes manifests ==="
kubectl apply -f namespace.yaml
kubectl apply -f db-deployment.yaml
kubectl apply -f db-service.yaml
kubectl apply -f web-deployment.yaml
kubectl apply -f web-service.yaml

echo "=== Deployment finished! ==="
kubectl get pods
kubectl get svc
