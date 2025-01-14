# Chat With PDF - Generative AI Application

This project demonstrates a serverless, AI-driven chatbot application that interacts with PDF documents. Built using **Amazon Bedrock**, **LangChain**, **Python**, and **Docker**, this application employs **Retrieval-Augmented Generation (RAG)** to provide context-based responses from a knowledge base. The solution includes two applications—Admin and User—designed for seamless document management and user interaction.

https://github.com/user-attachments/assets/bde43ff2-eb86-4f5f-b9a0-1f7d72f0be53


---

## Workflow
![image](https://github.com/user-attachments/assets/d0343dce-58df-41af-b4aa-b32ee21093aa)

## Features

### Admin Application
- Upload PDF documents via an intuitive web interface.
- Split PDF content into manageable chunks for efficient processing.
- Generate vector embeddings of document chunks using **Amazon Titan Embedding Model**.
- Store vector indices locally using **FAISS**.
- Upload vector indices to an **Amazon S3** bucket for centralized storage.

### User Application
- Query uploaded PDFs using a conversational interface.
- Retrieve vector indices from **Amazon S3** to rebuild a local **FAISS** index.
- Convert user queries to embeddings using **Amazon Titan Embedding Model**.
- Perform similarity searches on the FAISS index to fetch relevant context.
- Use **Anthropic Claude 2.1** for generating context-aware responses.

---

## Architecture Overview

The architecture consists of:
1. **Admin Application**: For PDF uploading, chunking, and vector embedding creation.
2. **User Application**: For querying PDFs and retrieving context-aware responses.
3. **Amazon Bedrock Services**:
   - **Titan Embedding Model** for vector embeddings.
   - **Anthropic Claude 2.1** for natural language processing.
4. **FAISS**: Local vector store for efficient similarity searches.
5. **Amazon S3**: For storing and retrieving vector indices.
6. **Docker**: Containerization for consistent deployment and scalability.

---

## Tech Stack

### AI Models
- **Amazon Titan Embedding G1 - Text**: For creating vector embeddings.
- **Anthropic Claude 2.1**: For generating conversational responses.

### Backend
- **Python**: Core application logic.
- **LangChain**: Manages document processing and retrieval workflows.
- **FAISS**: Efficient vector similarity search.

### Deployment
- **Docker**: Containerize applications for reliable and scalable deployment.
- **Amazon S3**: Centralized storage for vector indices.

### Monitoring
- **AWS CloudWatch**: For monitoring application performance and logging.

---

## Docker Workflow

### Admin Application
1. **Build Docker Image**:
   ```bash
   docker build -t pdf-reader-admin .
   ```
2. **Run Admin Application**:
   ```bash
   docker run -e BUCKET_NAME=<YOUR_S3_BUCKET_NAME> -v ~/.aws:/root/.aws -p 8083:8083 -it pdf-reader-admin
   ```

### User Application
1. **Build Docker Image**:
   ```bash
   docker build -t pdf-reader-user .
   ```
2. **Run User Application**:
   ```bash
   docker run -e BUCKET_NAME=<YOUR_S3_BUCKET_NAME> -v ~/.aws:/root/.aws -p 8084:8084 -it pdf-reader-user
   ```

---

## Usage

1. **Admin Application**:
   - Navigate to `http://localhost:8083`.
   - Upload a PDF document.
   - Confirm successful vector index creation and upload to S3.

2. **User Application**:
   - Navigate to `http://localhost:8084`.
   - Enter a query related to the uploaded document.
   - View AI-generated responses with relevant context.


