# Use an official lightweight Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required production dependencies
RUN pip install --no-cache-dir fastapi uvicorn httpx anthropic

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable placeholder for the enterprise client
ENV ANTHROPIC_API_KEY="placeholder-key-to-be-overridden-at-runtime"

# Run uvicorn server when the container launches
CMD ["uvicorn", "gateway_core:app", "--host", "0.0.0.0", "--port", "8000"]
