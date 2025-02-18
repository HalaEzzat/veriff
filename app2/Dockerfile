FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application code
COPY scraper.py .

# Install dependencies
RUN pip install --no-cache-dir requests psycopg2-binary

# Command to run the scraper
CMD ["python", "scraper.py"]