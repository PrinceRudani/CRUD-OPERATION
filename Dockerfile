FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY base/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose the Flask app port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
