#!/bin/bash
set -e  # Abort on error

# Load .env variables
set -o allexport
source .env
set +o allexport

FULL_IMAGE="southamerica-east1-docker.pkg.dev/${GCP_PROJECT_ID}/${GCP_REPO}/${GCP_IMAGE_NAME}:${GCP_IMAGE_TAG}"
FAD_RUN_JOB_NAME="fad-daily"
SCHEDULER_JOB_NAME1="fad-daily"
SVC_ACCOUNT="humboldt@${GCP_PROJECT_ID}.iam.gserviceaccount.com"
FAD_SCHEDULER_URI="https://${GCP_REGION}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${GCP_PROJECT_ID}/jobs/${FAD_RUN_JOB_NAME}:run"
AUDIENCE="https://${GCP_REGION}-run.googleapis.com"
SCHEDULE="0 * * * *"

#: <<'EOF'
# 1. Build and push Docker image
echo "Sending image to Artifact Registry..."
gcloud builds submit . --tag "$FULL_IMAGE"
#EOF

# 2. Create or update Cloud Run Jobs
if [ "$FAD_RUN_JOB_NAME" ]; then
  echo "Checking if Cloud Run Job '$FAD_RUN_JOB_NAME' exists..."
  if gcloud run jobs describe "$FAD_RUN_JOB_NAME" --region "$GCP_REGION" &> /dev/null; then
    echo "Job exists. Updating Cloud Run Job: $FAD_RUN_JOB_NAME"
    gcloud run jobs update "$FAD_RUN_JOB_NAME" \
      --image "$FULL_IMAGE" \
      --region "$GCP_REGION" \
      --env-vars-file=env-vars-daily.yaml

  else
    echo "Job does not exist. Creating Cloud Run Job: $FAD_RUN_JOB_NAME"
    gcloud run jobs create "$FAD_RUN_JOB_NAME" \
      --image "$FULL_IMAGE" \
      --region "$GCP_REGION" \
      --env-vars-file=env-vars-daily.yaml
  fi
fi

<<'EOF'
# 3. Grant invoker permission
echo "Checking invocation permission for: $SVC_ACCOUNT"
EXISTS=$(gcloud projects get-iam-policy "$GCP_PROJECT_ID" \
  --flatten="bindings[].members" \
  --format='table(bindings.role)' \
  --filter="bindings.members:serviceAccount:${SVC_ACCOUNT} AND bindings.role=roles/run.invoker" \
  | grep -c roles/run.invoker)

if [ "$EXISTS" -eq 0 ]; then
  echo "Permission does not exist - adding."
  gcloud projects add-iam-policy-binding "$GCP_PROJECT_ID" \
    --member="serviceAccount:${SVC_ACCOUNT}" \
    --role="roles/run.invoker" \
    --quiet
else
  echo "The roles/run.invoker permission is already assigned to $SVC_ACCOUNT"
fi

# 4. Create or update Cloud Scheduler Jobs
echo "Checking the existence of the Cloud Scheduler Job: $FAD_RUN_JOB_NAME"
if gcloud scheduler jobs describe "$FAD_RUN_JOB_NAME" --location="$GCP_REGION" &> /dev/null; then
  echo "Job exists, updating."
  gcloud scheduler jobs update http "$FAD_RUN_JOB_NAME" \
    --location="$GCP_REGION" \
    --schedule="$SCHEDULE" \
    --http-method=POST \
    --uri="$FAD_SCHEDULER_URI" \
    --oidc-service-account-email="$SVC_ACCOUNT" \
    --oidc-token-audience="$AUDIENCE"
else
  echo "Job doesn't exist, creating..."
  gcloud scheduler jobs create http "$FAD_RUN_JOB_NAME" \
    --location="$GCP_REGION" \
    --schedule="$SCHEDULE" \
    --http-method=POST \
    --uri="$FAD_SCHEDULER_URI" \
    --oidc-service-account-email="$SVC_ACCOUNT" \
    --oidc-token-audience="$AUDIENCE"
fi

# 5. Manually trigger Cloud Run jobs
echo "Manually triggering Cloud Run Job: $FAD_RUN_JOB_NAME"
gcloud run jobs execute "$FAD_RUN_JOB_NAME" --region="$GCP_REGION"
EOF
