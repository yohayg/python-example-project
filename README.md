

[![Coverage Status](https://coveralls.io/repos/github/yohayg/python-generator/badge.svg)](https://coveralls.io/github/yohayg/python-generator)
[![Build Status](https://travis-ci.org/yohayg/python-generator.svg?branch=master)](https://travis-ci.org/yohayg/python-generator)
[![Dependency Status](https://gemnasium.com/badges/github.com/yohayg/python-generator.svg)](https://gemnasium.com/github.com/yohayg/python-generator)

## Introduction

This project is a python command-line application example of generating data to csv.

## Prerequisites

* [docker](https://www.docker.com/)

## Running the Application

Clone:

    git clone https://github.com/yohayg/python-example-project.git
    
Run:

    docker-compose run csv-gen -r 1000 -o 1000.csv -b 1000 --verbose
Or install:
    
    pip install -e .
    csv-gen generate -r 1000 -o 1000.csv -b 1000 --verbose


##Example

![Alt Text](https://raw.githubusercontent.com/yohayg/python-generator/master/demo.gif)
    
## License

This project is licensed under [MIT license](http://opensource.org/licenses/MIT).    
