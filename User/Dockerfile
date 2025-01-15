FROM python:3.11
# Set the AWS region as an environment variable
ENV AWS_DEFAULT_REGION=us-west-2
ENV AWS_ACCESS_KEY_ID=
ENV AWS_SECRET_ACCESS_KEY=

EXPOSE 8084
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . ./
# Ensure Streamlit config file is in the correct location
RUN mkdir -p ~/.streamlit
COPY .streamlit/config.toml ~/.streamlit/config.toml
ENTRYPOINT [ "streamlit", "run", "app.py", "--server.port=8084", "--server.address=0.0.0.0" ]
