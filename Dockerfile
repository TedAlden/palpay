FROM python:3.13-bookworm

WORKDIR /app

# Install build dependencies needed for Thriftpy2 server
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/

RUN pip install -r requirements.txt

# Copy the Django appl
COPY ./webapps2025/ /app/

# Expose the port the app runs on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
