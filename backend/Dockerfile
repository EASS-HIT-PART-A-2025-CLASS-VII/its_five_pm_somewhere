# Use official Python image
FROM python:3.13-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire app and tests (to run tests inside container)
COPY app ./app
COPY tests ./tests

EXPOSE 8000

# Run FastAPI app 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
