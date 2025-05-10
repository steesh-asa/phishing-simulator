#Use the official Python image from Docker Hub
FROM python:3.9

#Set the working directory inside the container
WORKDIR /app

#Copy the requirements file into the container
COPY requirements.txt /app/

#Install the required Python packages
RUN pip install -r requirements.txt

#Copy the rest of the application code
COPY . /app/

#Epose the port Flask app will run on
EXPOSE 5000

#Runt the flask app
CMD ["python", "app.py"]
