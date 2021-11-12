# syntax=docker/dockerfile:1

# Base image
FROM python:latest

# Use app as a default location for all the subsequent commands
WORKDIR /pokedex

# Copy source code
COPY src src

# Install requirements and prepare the environment
COPY requirements.txt requirements.txt
COPY setup.py setup.py
RUN pip install -r requirements.txt
RUN pip install -e .

ENV FLASK_APP "pokedex"

# Run the web server
WORKDIR /pokedex/src
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "6000"]
