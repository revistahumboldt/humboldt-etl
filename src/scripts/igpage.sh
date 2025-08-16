#!/bin/bash
set -e  # Abort on error

# Load .env variables
set -o allexport
source .env
set +o allexport

FULL_IMAGE="southamerica-east1-docker.pkg.dev/${GCP_PROJECT_ID}/${GCP_REPO}/${GCP_IMAGE_NAME}:${GCP_IMAGE_TAG}"
RUN_JOB_NAME="igpage-daily"
SCHEDULER_JOB_NAME="igpage-daily"
SVC_ACCOUNT="humboldt@${GCP_PROJECT_ID}.iam.gserviceaccount.com"
FAD_SCHEDULER_URI="https://${GCP_REGION}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${GCP_PROJECT_ID}/jobs/${RUN_JOB_NAME}:run"
AUDIENCE="https://${GCP_REGION}-run.googleapis.com"
SCHEDULE="0 14 * * *"

# 1. Create or update Cloud Run Jobs
if [ "$RUN_JOB_NAME" ]; then
  echo "Checking if Cloud Run Job '$RUN_JOB_NAME' exists..."
  if gcloud run jobs describe "$RUN_JOB_NAME" --region "$GCP_REGION" &> /dev/null; then
    echo "Job exists. Updating Cloud Run Job: $RUN_JOB_NAME"
    gcloud run jobs update "$RUN_JOB_NAME" \
      --image "$FULL_IMAGE" \
      --region "$GCP_REGION" \
      --env-vars-file=env-vars-igpage.yaml

  else
    echo "Job does not exist. Creating Cloud Run Job: $RUN_JOB_NAME"
    gcloud run jobs create "$RUN_JOB_NAME" \
      --image "$FULL_IMAGE" \
      --region "$GCP_REGION" \
      --env-vars-file=env-vars-igpage.yaml
  fi
fi

# 2. Manually trigger Cloud Run jobs
echo "Manually triggering Cloud Run Job: $RUN_JOB_NAME"
gcloud run jobs execute "$RUN_JOB_NAME" --region="$GCP_REGION"

