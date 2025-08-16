#!/bin/bash
set -e  # Abort on error

# Load .env variables
set -o allexport
source .env
set +o allexport

SVC_ACCOUNT="humboldt@${GCP_PROJECT_ID}.iam.gserviceaccount.com"


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
