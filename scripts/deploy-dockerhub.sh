#!/usr/bin/env bash
set -euo pipefail

# Usage:
# DOCKERHUB_USER=youruser DOCKERHUB_REPO=discord-plateau-bot TAG=latest ./scripts/deploy-dockerhub.sh

: "${DOCKERHUB_USER?Please set DOCKERHUB_USER (ex: your Docker Hub username)}"
: "${DOCKERHUB_REPO?Please set DOCKERHUB_REPO (ex: discord-plateau-bot)}"

TAG="${TAG:-latest}"
IMAGE="${DOCKERHUB_USER}/${DOCKERHUB_REPO}:${TAG}"

echo "Building Docker image: ${IMAGE}"
docker build -t "${IMAGE}" .

echo "Checking Docker login..."
if ! docker info >/dev/null 2>&1; then
  echo "Docker doesn't seem available or you are not logged in. Please run: docker login" >&2
  exit 1
fi

echo "Pushing image to Docker Hub: ${IMAGE}"
docker push "${IMAGE}"

echo "Push complete. You can now pull with: docker pull ${IMAGE}"

echo "Tip: On Synology Container Manager, use the same image name: ${IMAGE} and set environment variables as in .env.example"
