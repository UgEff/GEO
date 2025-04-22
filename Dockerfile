FROM python:3.10-slim

# Avoid creating .pyc files and disable buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define working directory
WORKDIR /app

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install requests python-dotenv geopy pandas psycopg2-binary

# Copy code source
COPY . /app

# Run the script
CMD ["python", "app/main.py"] 