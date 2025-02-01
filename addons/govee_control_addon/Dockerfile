FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy dependency definitions and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY main.py .

# Expose the port that matches the add-on config (5000)
EXPOSE 5000

# Run the application
CMD [ "python", "main.py" ]
