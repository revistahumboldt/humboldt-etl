#!/bin/bash

set -e  # To abort in error

# Loads the .env variables into the environment
set -o allexport
source .env
set +o allexport

FULL_IMAGE="southamerica-east1-docker.pkg.dev/${GCP_PROJECT_ID}/${GCP_REPO}/${GCP_IMAGE_NAME}:${GCP_IMAGE_TAG}"

RUN_JOB_NAME="fad-gender-age"
SCHEDULER_JOB_NAME="fad-gender-age-scheduler-trigger"
SVC_ACCOUNT="humboldt@${GCP_PROJECT_ID}.iam.gserviceaccount.com"
SCHEDULER_URI="https://${GCP_REGION}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${GCP_PROJECT_ID}/jobs/${RUN_JOB_NAME}:run"
AUDIENCE="https://${GCP_REGION}-run.googleapis.com"
SCHEDULE="0 * * * *"

: <<'EOF'
# 1. Build e upload da imagem Docker
echo "Sending image to Artifact Registry..."
gcloud builds submit . --tag "$FULL_IMAGE"

# 2. Update Cloud Run Job
echo "Updating Cloud Run Job: $RUN_JOB_NAME"
gcloud run jobs update "$RUN_JOB_NAME" \
  --image "$FULL_IMAGE" \
  --region "$GCP_REGION" \
  --set-env-vars="META_AD_ACCOUNT_ID=${META_AD_ACCOUNT_ID},GCP_PROJECT_ID=${GCP_PROJECT_ID},BQ_DATASET_ID=${BQ_DATASET_ID},BQ_TABLE_ID=${BQ_TABLE_ID},META_APP_ID=${META_APP_ID},META_APP_SECRET=${META_APP_SECRET},WINDOW=daily,META_ACCESS_TOKEN=${META_ACCESS_TOKEN}"
EOF

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

# 4. Criar ou atualizar Cloud Scheduler Job
echo "Checking the existence of the Cloud Scheduler Job:$SCHEDULER_JOB_NAME"
if gcloud scheduler jobs describe "$SCHEDULER_JOB_NAME" --location="$GCP_REGION" &> /dev/null; then
  echo "Job exists, updating."
  gcloud scheduler jobs update http "$SCHEDULER_JOB_NAME" \
    --location="$GCP_REGION" \
    --schedule="$SCHEDULE" \
    --http-method=POST \
    --uri="$SCHEDULER_URI" \
    --oidc-service-account-email="$SVC_ACCOUNT" \
    --oidc-token-audience="$AUDIENCE"
else
  echo "Job doesn't exist, creating..."
  gcloud scheduler jobs create http "$SCHEDULER_JOB_NAME" \
    --location="$GCP_REGION" \
    --schedule="$SCHEDULE" \
    --http-method=POST \
    --uri="$SCHEDULER_URI" \
    --oidc-service-account-email="$SVC_ACCOUNT" \
    --oidc-token-audience="$AUDIENCE"
fi

: <<'EOF'
# 5. Disparar o trabalho do Cloud Run Scheduler
echo "Runing job via Cloud Scheduler endpoint."
TOKEN=$(gcloud auth print-access-token --impersonate-service-account="$SVC_ACCOUNT")

curl -X POST "$SCHEDULER_URI" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'

echo "Cloud Scheduler trigger successfully simulated."
EOF

# 5. Disparar o Cloud Run job 
echo "Manually triggering cloud run job"
gcloud run jobs execute "$SCHEDULER_JOB_NAME" --region="$REGION"

