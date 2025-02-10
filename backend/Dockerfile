# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the container
COPY . .

# Expose port 8000 for Django
EXPOSE 8000

# Start Django using the built-in server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "adaptive_learning.wsgi:application"]
