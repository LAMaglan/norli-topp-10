# Get base image
FROM python:3.10-buster

# technically not necessary in my case, but maybe b/c python command makes it?
RUN mkdir /output

# Copy the Python requirements file to the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script to the container
COPY main.py .

# Run the Python script and generate the CSV file
CMD [ "python", "main.py"]