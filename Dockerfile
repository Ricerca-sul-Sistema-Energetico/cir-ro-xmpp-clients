# set base image (host OS)
FROM python:3.11
# FROM python:3.11-slim

# set the working directory in the container to /src
WORKDIR /app

# copy and install dependencies file to working directory
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# copy the config file to working directory

# copy the content of the local src directory to the working directory
COPY src .
COPY .env .env


# Comando per avviare il server FastAPI con uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
