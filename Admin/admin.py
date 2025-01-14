import streamlit as st
import os
import uuid
import boto3
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import FAISS

# Initialization
s3_client = boto3.client("s3")
BUCKET_NAME = os.getenv("BUCKET_NAME")
folder_path = "/tmp/"
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0", client=boto3.client(service_name="bedrock-runtime"))

# Helper Functions
def upload_file_to_s3(file):
    unique_file_name = f"{get_unique_id()}_{file.name}"
    file_path = os.path.join(folder_path, unique_file_name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    s3_client.upload_file(Filename=file_path, Bucket=BUCKET_NAME, Key=unique_file_name)
    return unique_file_name

def get_unique_id():
    return str(uuid.uuid4())

def rebuild_index():
    # Logic for rebuilding the FAISS index with the latest data
    st.info("Rebuilding the index... (This is a placeholder)")

def list_s3_files():
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    return [file["Key"] for file in response.get("Contents", [])]

# Main Admin Application
def admin_main():
    st.title("⚙️ **Admin Dashboard**")
    st.markdown("Welcome to the Admin Panel. Use the tools below to manage resources and monitor the chatbot.")

    # Button to go back to the user chatbot
    if st.button("💬 Go to User Chatbot"):
        st.markdown("""
            <meta http-equiv="refresh" content="0; url=http://localhost:8084/">
        """, unsafe_allow_html=True)

    # Tabs for different admin functionalities
    tab1, tab2, tab3 = st.tabs(
        ["📂 **Manage Files**", "🔄 **Index Management**", "📊 **Query Logs**"]
    )

    # Tab 1: Manage Files
    with tab1:
        st.header("📂 **Upload and Manage Files**")
        st.markdown(
            "Upload files to update the chatbot's knowledge base. The uploaded files will be stored in the S3 bucket."
        )

        # Upload file section
        uploaded_file = st.file_uploader("📤 Upload a new file", type=["pdf", "txt", "csv"])
        if uploaded_file:
            with st.spinner("Uploading file..."):
                file_name = upload_file_to_s3(uploaded_file)
                st.success(f"✅ File `{file_name}` uploaded successfully!")

        # Display existing files
        st.subheader("🗂️ **Existing Files in S3**")
        s3_files = list_s3_files()
        if s3_files:
            for file in s3_files:
                st.write(f"📄 {file}")
        else:
            st.info("ℹ️ No files found in the S3 bucket.")

    # Tab 2: Index Management
    with tab2:
        st.header("🔄 **Index Management**")
        st.markdown(
            "Reload or rebuild the FAISS index to ensure the chatbot uses the latest information."
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔃 Reload Index"):
                with st.spinner("Reloading the FAISS index..."):
                    load_index()
                    st.success("✅ Index reloaded successfully!")
        with col2:
            if st.button("⚙️ Rebuild Index"):
                with st.spinner("Rebuilding the index..."):
                    rebuild_index()
                    st.success("✅ Index rebuilt successfully!")

    # Tab 3: Query Logs
    with tab3:
        st.header("📊 **Query Logs and Monitoring**")
        st.markdown("Monitor chatbot queries for analysis and debugging.")

        # Placeholder for logs - Replace with actual log retrieval
        logs = [
            {"timestamp": "2024-12-30 10:00", "question": "What is AI?", "status": "Success"},
            {"timestamp": "2024-12-30 10:15", "question": "Explain ML?", "status": "Success"},
        ]

        if logs:
            for log in logs:
                st.write(
                    f"🕒 `{log['timestamp']}` - **Question**: {log['question']} - **Status**: {log['status']}"
                )
        else:
            st.info("ℹ️ No logs available.")

# Run Admin Application
if __name__ == "__main__":
    admin_main()
