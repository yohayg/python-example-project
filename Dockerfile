FROM python:2.7-alpine

# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Bundle app source
#COPY . /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir  -r requirements.txt

ENTRYPOINT [ "python","-u", "project" ]
