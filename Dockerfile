FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the .env file into the container at /app
COPY .env /app/.env

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "letscodetogether_moderator.py"]