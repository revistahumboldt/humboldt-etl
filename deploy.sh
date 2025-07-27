#!/bin/bash
set -e  # Abort on error

# Load .env variables
set -o allexport
source .env
set +o allexport

FULL_IMAGE="southamerica-east1-docker.pkg.dev/${GCP_PROJECT_ID}/${GCP_REPO}/${GCP_IMAGE_NAME}:${GCP_IMAGE_TAG}"

RUN_JOB_NAME1="fad-gender-age"
RUN_JOB_NAME2="fad-platform"

SCHEDULER_JOB_NAME1="fad-gender-age-scheduler-trigger"
SCHEDULER_JOB_NAME2="fad-platform-scheduler-trigger"

SVC_ACCOUNT="humboldt@${GCP_PROJECT_ID}.iam.gserviceaccount.com"

SCHEDULER_URI1="https://${GCP_REGION}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${GCP_PROJECT_ID}/jobs/${RUN_JOB_NAME1}:run"
SCHEDULER_URI2="https://${GCP_REGION}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${GCP_PROJECT_ID}/jobs/${RUN_JOB_NAME2}:run"

AUDIENCE="https://${GCP_REGION}-run.googleapis.com"
SCHEDULE="0 * * * *"

: <<'EOF'
# 1. Build and push Docker image
echo "Sending image to Artifact Registry..."
gcloud builds submit . --tag "$FULL_IMAGE"
EOF

# 2. Create or update Cloud Run Jobs
if [ "$RUN_JOB_NAME1" ]; then
  echo "Checking if Cloud Run Job '$RUN_JOB_NAME1' exists..."
  if gcloud run jobs describe "$RUN_JOB_NAME1" --region "$GCP_REGION" &> /dev/null; then
    echo "Job exists. Updating Cloud Run Job: $RUN_JOB_NAME1"
    gcloud run jobs update "$RUN_JOB_NAME1" \
      --image "$FULL_IMAGE" \
      --region "$GCP_REGION" \
      --env-vars-file=env-vars-age-gender.yaml

  else
    echo "Job does not exist. Creating Cloud Run Job: $RUN_JOB_NAME1"
    gcloud run jobs create "$RUN_JOB_NAME1" \
      --image "$FULL_IMAGE" \
      --region "$GCP_REGION" \
      --env-vars-file=env-vars-age-gender.yaml
  fi
fi


if [ "$RUN_JOB_NAME2" ]; then
  echo "Checking if Cloud Run Job '$RUN_JOB_NAME2' exists..."
  if gcloud run jobs describe "$RUN_JOB_NAME2" --region "$GCP_REGION" &> /dev/null; then
    echo "Job exists. Updating Cloud Run Job: $RUN_JOB_NAME2"
    gcloud run jobs update "$RUN_JOB_NAME2" \
      --image "$FULL_IMAGE" \
      --region "$GCP_REGION" \
      --env-vars-file=env-vars-platform.yaml

  else
    echo "Job does not exist. Creating Cloud Run Job: $RUN_JOB_NAME2"
    gcloud run jobs create "$RUN_JOB_NAME2" \
      --image "$FULL_IMAGE" \
      --region "$GCP_REGION" \
      --env-vars-file=env-vars-platform.yaml

  fi
fi

: <<'EOF'
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
echo "Checking the existence of the Cloud Scheduler Job: $SCHEDULER_JOB_NAME1"
if gcloud scheduler jobs describe "$SCHEDULER_JOB_NAME1" --location="$GCP_REGION" &> /dev/null; then
  echo "Job exists, updating."
  gcloud scheduler jobs update http "$SCHEDULER_JOB_NAME1" \
    --location="$GCP_REGION" \
    --schedule="$SCHEDULE" \
    --http-method=POST \
    --uri="$SCHEDULER_URI1" \
    --oidc-service-account-email="$SVC_ACCOUNT" \
    --oidc-token-audience="$AUDIENCE"
else
  echo "Job doesn't exist, creating..."
  gcloud scheduler jobs create http "$SCHEDULER_JOB_NAME1" \
    --location="$GCP_REGION" \
    --schedule="$SCHEDULE" \
    --http-method=POST \
    --uri="$SCHEDULER_URI1" \
    --oidc-service-account-email="$SVC_ACCOUNT" \
    --oidc-token-audience="$AUDIENCE"
fi

echo "Checking the existence of the Cloud Scheduler Job: $SCHEDULER_JOB_NAME2"
if gcloud scheduler jobs describe "$SCHEDULER_JOB_NAME2" --location="$GCP_REGION" &> /dev/null; then
  echo "Job exists, updating."
  gcloud scheduler jobs update http "$SCHEDULER_JOB_NAME2" \
    --location="$GCP_REGION" \
    --schedule="$SCHEDULE" \
    --http-method=POST \
    --uri="$SCHEDULER_URI2" \
    --oidc-service-account-email="$SVC_ACCOUNT" \
    --oidc-token-audience="$AUDIENCE"
else
  echo "Job doesn't exist, creating..."
  gcloud scheduler jobs create http "$SCHEDULER_JOB_NAME2" \
    --location="$GCP_REGION" \
    --schedule="$SCHEDULE" \
    --http-method=POST \
    --uri="$SCHEDULER_URI2" \
    --oidc-service-account-email="$SVC_ACCOUNT" \
    --oidc-token-audience="$AUDIENCE"
fi
EOF

# 5. Manually trigger Cloud Run jobs
echo "Manually triggering Cloud Run Job: $RUN_JOB_NAME1"
gcloud run jobs execute "$RUN_JOB_NAME1" --region="$GCP_REGION"

echo "Manually triggering Cloud Run Job: $RUN_JOB_NAME2"
gcloud run jobs execute "$RUN_JOB_NAME2" --region="$GCP_REGION"
