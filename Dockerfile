# Use the latest official Python image as the base image
FROM python:latest

# Set the working directory inside the container
WORKDIR /app

# Install dependencies from requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Install necessary tools for curl, vim, and dos2unix
RUN apt-get update && apt-get install -y curl vim dos2unix bash

RUN curl -fsSL https://ollama.com/install.sh | sh


# Expose Flask and Ollama ports
EXPOSE 5000
EXPOSE 11434

# Copy the application code into the container
COPY . /app/

# Run Ollama and Flask app
CMD ["bash", "-c", "ollama run llama3 &  ollama pull nomic-embed-text & python app.py"]
