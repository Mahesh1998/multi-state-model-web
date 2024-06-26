# Use an official Python runtime as a parent image
FROM python:3.12.3-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory for subsequent instructions
WORKDIR /app/prediction_of_charge_delocalization_in_oligomer

# List files in the current directory (optional for debugging)
# RUN ls -l

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
