# Use an official Ubuntu as a parent image
FROM ubuntu:20.04

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Python and other necessary packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    clamav \
    clamav-daemon \
    && rm -rf /var/lib/apt/lists/*

# Update ClamAV database
RUN freshclam

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Ensure ClamAV daemon runs
RUN sed -i 's/^Example/#Example/' /etc/clamav/clamd.conf

# Make port 80 available to the world outside this container
EXPOSE 80

# Run ClamAV daemon and the bot script
CMD service clamav-daemon start && python3 main.py
