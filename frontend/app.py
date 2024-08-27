
import os
import requests
import streamlit as st


NGINX_HOST = os.getenv("NGINX_HOST")

st.title("PDF Search Engine")


# File Upload Section
st.header("Upload Document")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    if st.button("Upload"):
        with st.spinner("Uploading file..."):
            # Get presigned URL from backend
            response = requests.get(f"http://{NGINX_HOST}/upload/get-presigned-url", 
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
                    ingestion_response = requests.post(f"http://{NGINX_HOST}/upload/initiate-processing", json={"jobId": job_id, "s3Key": s3_key})
                    ingestion_response.raise_for_status()

                    st.success(f"File uploaded successfully! Job ID: {job_id}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to upload file: {e}")
            else:
                st.error(f"Failed to get presigned URL: {response.text}")   


# Query Section
st.header("Query Document")
query = st.text_input("Enter your query:")

if st.button("Submit Query"):
    if query:
        with st.spinner("Processing query..."):
            try:
                response = requests.post(f"http://{NGINX_HOST}/query", json={"query": query})
                response.raise_for_status()
                result = response.json()

                st.subheader("Answer:")
                st.write(result["response"])

                st.subheader("Sources:")
                unique_sources = list(set(result["sources"]))
                for source in unique_sources:
                    st.write(source)
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to get query response: {e}")
    else:
        st.warning("Please enter a query before submitting.")