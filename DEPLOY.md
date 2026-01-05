# Deployment Guide: Firebase & Cloud Run

This guide explains how to deploy your Flask application to **Google Cloud Run** and serve it via **Firebase Hosting**.

## Prerequisites

1.  **Google Cloud SDK (`gcloud`)**: Installed and initialized.
2.  **Firebase CLI**: Installed (`npm install -g firebase-tools`).
3.  **Google Cloud Project**: Created with billing enabled (required for Cloud Run).

## Step 1: Initialize Setup

1.  Login to Google Cloud:
    ```bash
    gcloud auth login
    gcloud config set project YOUR_PROJECT_ID
    ```
2.  Login to Firebase:
    ```bash
    firebase login
    firebase use YOUR_PROJECT_ID
    ```
    *(Replace `YOUR_PROJECT_ID` with your actual project ID from the Firebase Console).*

## Step 2: Build and Deploy Backend (Cloud Run)

1.  Submit the build to Cloud Build (or build locally if you have Docker):
    ```bash
    gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/resume-authentication
    ```
2.  Deploy to Cloud Run:
    ```bash
    gcloud run deploy resume-authentication \
      --image gcr.io/YOUR_PROJECT_ID/resume-authentication \
      --platform managed \
      --region us-central1 \
      --allow-unauthenticated
    ```
    *Note: This creates a service named `resume-authentication`. If you choose a different name, update `firebase.json`.*

## Step 3: Configure Environment Variables

Since we are not using a `.env` file in production, set the secrets in Cloud Run:

```bash
gcloud run services update resume-authentication \
  --set-env-vars "SECRET_KEY=your_production_secret_key,GEMINI_API_KEY=your_gemini_api_key" \
  --region us-central1
```

## Step 4: Connect Firebase Hosting

1.  Deploy the hosting configuration (which proxies to Cloud Run):
    ```bash
    firebase deploy --only hosting
    ```

## Ephemeral Storage Warning

**Important**: Cloud Run has an **ephemeral filesystem**.
- Files uploaded to `data/temp_uploads` will vanish when the container restarts.
- New users registered in `data/users.json` will be lost on the next deployment.

For a permanent solution, you must modify the code to use **Cloud Storage** for files and **Firestore** for the database.
