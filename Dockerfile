# Use the official Python image as the base image
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE OrderDelaySystem.settings

# Create and set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files to the container's working directory
COPY . /app/

# Run the makemigrations and migrate commands
RUN python manage.py makemigrations
RUN python manage.py migrate

# Expose the port that the Django app runs on
EXPOSE 8000

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
