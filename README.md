

[![Coverage Status](https://coveralls.io/repos/github/yohayg/python-generator/badge.svg)](https://coveralls.io/github/yohayg/python-generator)
[![Build Status](https://travis-ci.org/yohayg/python-generator.svg?branch=master)](https://travis-ci.org/yohayg/python-generator)

## Introduction

This project is a python command-line application example of generating data to csv.

## Running the Application

#### Clone:

    git clone https://github.com/yohayg/python-example-project.git
    
#### Install:
    
    pip install -r requirements.txt

#### Run:
    
    python -m project mp -o 1000.csv -r 1000 -b 1000 
Or:
    
    python -m project rx -o 1000.csv -r 1000 -b 1000
Or:

    python -m project se -o 1000.csv -r 1000 -b 1000
Or:

    docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3
    celery -A project.lib.celery_app:app  worker --loglevel=debug -B -l info
    python -m project.lib.rabbit_mq_listener
    python -m project ce  -r 100 -b 10


#### Test:

    pip install -r test/requirements.txt
    python project/tests

## License

This project is licensed under [MIT license](http://opensource.org/licenses/MIT).    
