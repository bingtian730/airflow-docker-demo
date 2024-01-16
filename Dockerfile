# Use the official Airflow image as the base image
# Use the official Airflow image as the base image
FROM python:3.10
FROM apache/airflow:2.7.3


# Set the Python version to 3.10
ARG PYTHON_VERSION=3.10

ENV PYTHONPATH=/

# Install Python 3.10
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#         python${PYTHON_VERSION} \
#         python${PYTHON_VERSION}-dev \
#         python${PYTHON_VERSION}-pip && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/* && \
#     update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${PYTHON_VERSION} 1 && \
#     update-alternatives --install /usr/bin/python python /usr/bin/python${PYTHON_VERSION} 1

# Upgrade pip
RUN python -m pip install --upgrade pip

# # Continue with the rest of the original Dockerfile content

# RUN pipenv sync
# RUN pipenv shell

# Install additional dependencies from requirements.txt
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN pip install operators

# Continue with the rest of the original Dockerfile content
