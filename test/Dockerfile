FROM  python:2.7-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /tmp/requirements.txt

#RUN apk add --no-cache gcc libc-dev unixodbc-dev
#RUN pip install --upgrade pip

RUN apk --update add python py-pip openssl ca-certificates py-openssl wget
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base \
  && pip install --upgrade pip \
  && pip install -r /tmp/requirements.txt \
  && apk del build-dependencies

#COPY requirements.txt /tmp/requirements.txt
#RUN pip install --no-cache-dir -r /tmp/requirements.txt
#RUN python setup.py install
#CMD ["python", "./project/tests"]
#CMD ["coverage", "run", "setup.py test"]