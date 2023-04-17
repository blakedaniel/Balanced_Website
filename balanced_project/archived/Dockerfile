## python setup
FROM python:3.11.2

# ensure python output is sent straight to terminal
ENV PYTHONBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# set working directory
WORKDIR /code

# copy project
COPY . /code/

# update pip
RUN pip install --upgrade pip

# install dependencies
RUN pip install -r requirements.txt

# activate virtual environment and run server through startup script
CMD bash bin/startup.sh