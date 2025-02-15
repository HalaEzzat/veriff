# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY app.py /app/

# Install dependencies
RUN pip install flask

# Expose port 80
EXPOSE 80

# Run the app
CMD ["python", "app.py"]
