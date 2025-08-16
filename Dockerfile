
# Use an official Python 3.11 base image (slim-buster is good for small size)
FROM python:3.11-slim-buster

# Defines the working directory inside the container
# All subsequent commands will be executed from this directory
WORKDIR /app

# Copy the dependencies file (requirements.txt) and install it
# We do this first to take advantage of Docker's cache.
# If requirements.txt doesn't change, this layer won't be rebuilt.
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# Copies all your application code to the /app working directory
# The '.' at the end means "copy everything from the current (local) directory to the WORKDIR (container)"
# This will include main.py, src/, utils/, .env (if it's in the local root)
COPY . .

# Defines the command that will be executed when the container starts
# Since main.py is in the root of your project and you copied the 'src' folder to /app,
# the path to your main script inside the container will be /app/src/main.py.
CMD ["python", "src/main.py"]

# Observations:
# - It is not necessary to configure ports (such as 8080) or Gunicorn for a Cloud Run Job,
# because it doesn't serve HTTP traffic, it just runs a process.
# - For sensitive environment variables, use the Google Cloud Secret Manager
# instead of including them directly in the Dockerfile or .env inside the image
# (although for initial development, the .env can be copied).