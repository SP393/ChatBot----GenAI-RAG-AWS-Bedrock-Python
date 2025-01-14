import streamlit as st
import os
import uuid
import boto3
from langchain_community.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS

# Initialization
s3_client = boto3.client("s3")
bedrock_client = boto3.client(service_name="bedrock-runtime")
BUCKET_NAME = os.getenv("BUCKET_NAME")
folder_path = "/tmp/"

bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0", client=bedrock_client)

# Helper Functions
def get_unique_id():
    return str(uuid.uuid4())

def load_index():
    s3_client.download_file(Bucket=BUCKET_NAME, Key="my_faiss.faiss", Filename=f"{folder_path}my_faiss.faiss")
    s3_client.download_file(Bucket=BUCKET_NAME, Key="my_faiss.pkl", Filename=f"{folder_path}my_faiss.pkl")

def get_llm():
    return Bedrock(model_id="anthropic.claude-v2:1", client=bedrock_client, model_kwargs={'max_tokens_to_sample': 512})

def get_response(llm, vectorstore, question):
    prompt_template = """
    Human: Please use the given context to provide concise answer to the question
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    <context>
    {context}
    </context>
    Question: {question}
    Assistant:"""
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )
    answer = qa({"query": question})
    return answer['result']

# Admin Login Page
def admin_login():
    st.title("🔒 Admin Login")
    st.markdown("Please log in to access the admin dashboard.")
    
    # Simple login form
    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")
    
    if st.button("Log In"):
        if username == "admin" and password == "admin@123":  # Replace with your credentials
            st.session_state["is_admin"] = True
            st.success("✅ Login successful!")
            # Redirect to the desired URL
            st.markdown("""
                <meta http-equiv="refresh" content="0; url=http://localhost:8083/">
            """, unsafe_allow_html=True)
        else:
            st.error("❌ Incorrect username or password.")


# Main Application
def main():
    # Handle navigation between chatbot and admin login
    st.sidebar.title("Navigation")
    if st.sidebar.button("🔒 Login as Admin"):
        st.session_state["page"] = "admin"
    
    if st.session_state.get("page") == "admin":
        admin_login()
    else:
        st.title("🤖 AI-Powered Chatbot")
        st.markdown("Welcome! Ask any question and I'll provide the most relevant answer using advanced AI models. 🌟")
        
        # Load index
        with st.spinner("Loading resources..."):
            load_index()
        
        # Create Index
        faiss_index = FAISS.load_local(
            index_name="my_faiss",
            folder_path=folder_path,
            embeddings=bedrock_embeddings,
            allow_dangerous_deserialization=True
        )
        
        # Input Section
        with st.form("question_form"):
            question = st.text_input("🔍 **Ask your question here**:")
            submit_button = st.form_submit_button("💬 Ask")
        
        # Response Section
        if submit_button:
            with st.spinner("Querying the AI..."):
                llm = get_llm()
                response = get_response(llm, faiss_index, question)
                st.markdown("### 💡 **Answer**")
                st.success(response)
                st.balloons()

# Run Application
if __name__ == "__main__":
    if "is_admin" not in st.session_state:
        st.session_state["is_admin"] = False
    if "page" not in st.session_state:
        st.session_state["page"] = "chatbot"
    
    main()
