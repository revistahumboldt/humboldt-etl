#!/bin/bash
set -e  # Abort on error

# Load .env variables
set -o allexport
source .env
set +o allexport
FULL_IMAGE="southamerica-east1-docker.pkg.dev/${GCP_PROJECT_ID}/${GCP_REPO}/${GCP_IMAGE_NAME}:${GCP_IMAGE_TAG}"

#: <<'EOF'
# 1. Build and push Docker image
echo "Sending image to Artifact Registry..."
gcloud builds submit . --tag "$FULL_IMAGE"
#EOF