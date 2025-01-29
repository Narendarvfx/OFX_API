# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /ofx_api

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN apt-get update \
    && apt-get install -y default-mysql-client \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
#ENV DJANGO_SETTINGS_MODULE=OFX_API.settings

# Run the Django development server
CMD ["gunicorn", "OFX_API.wsgi:application", "--bind", "0.0.0.0:8000" ]
