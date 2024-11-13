# python/3.10/bullseye
# pip install pipenv
# pipenv install
# pipenv run python run.py

# Use the official Python 3.10 image based on Debian Bullseye
FROM python:3.10-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy Pipfile and Pipfile.lock to the working directory
COPY Pipfile Pipfile.lock ./

# Install pipenv
RUN pip install pipenv

# Install dependencies using pipenv
RUN pipenv install --system --deploy

# Copy the rest of the application code
COPY . .

# Expose the desired port (e.g., 5000 if Flask, or 8000 for Django)
EXPOSE 8080

# Set the default command to run the application
CMD ["pipenv", "run", "python", "run.py"]
