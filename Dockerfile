# # Pull base image
# FROM python:3.12.5-slim

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Set work directory
# WORKDIR /app

# #install dependencies
# RUN pip install --upgrade pip
# COPY /requirement/base.txt/ .
# RUN pip install -r base.txt

# # Copy project
# COPY . .


# Pull base image
FROM python:3.12.5-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/

# Install dependencies
COPY requirement/base.txt ./
RUN pip install --upgrade pip
RUN pip install -r base.txt

# Copy project files
COPY . .


# Optional: Set a default command, for example to run a Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
