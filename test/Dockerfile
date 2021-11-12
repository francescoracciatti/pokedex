# syntax=docker/dockerfile:1

# Base image
FROM python:latest

# Use app as a default location for all the subsequent commands
WORKDIR /test

# Copy source code
COPY . .

# Install requirements and prepare the environment
RUN pip install -r requirements.txt

# Run the tests
CMD ["python", "test_api.py", "--host", "127.0.0.1", "--port", "6000", "TestAPI"]
