# pull base image
FROM python:3.7

RUN apt-get update && apt-get -y install libpq-dev

# Set work directory
WORKDIR /app

# Install dependencies
ADD ./requirements.txt /app/
RUN pip install -r requirements.txt 

# set environment varibles
ADD ./apps /app/apps
ADD ./todoapp /app/todoapp 
ADD manage.py /app/

CMD ["python", "manage.py", "runserver", "0:8000"
