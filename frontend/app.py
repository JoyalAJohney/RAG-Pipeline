
import os
import requests
import streamlit as st


UPLOAD_SERVICE_URL = os.getenv("UPLOAD_SERVICE_URL")

st.title("Document Upload")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    if st.button("Upload"):
        
        # Get presigned URL from backend
        response = requests.get(f"{UPLOAD_SERVICE_URL}/get-presigned-url", 
            params={"fileName": uploaded_file.name, "fileType": uploaded_file.type})
        
        if response.status_code == 200:
            presigned_data = response.json()
            presigned_url = presigned_data["presignedUrl"]
            job_id = presigned_data["jobId"]
            s3_key = presigned_data["s3Key"]

            # Upload file to S3
            try:
                response = requests.put(presigned_url, data=uploaded_file.getvalue(), headers={"Content-Type": uploaded_file.type})
                response.raise_for_status() # Raise an exception if the request fails

                # Notify backend to start processing the file
                ingestion_response = requests.post(f"{UPLOAD_SERVICE_URL}/initiate-processing", json={"jobId": job_id, "s3Key": s3_key})
                ingestion_response.raise_for_status()

                st.success(f"File uploaded successfully! Job ID: {job_id}")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to upload file: {e}")
        else:
            st.error(f"Failed to get presigned URL: {response.text}")   