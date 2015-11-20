#!/bin/bash

# -*- ENCODING: UTF-8 -*-
#echo "Introduce tu puerto : "
#read puerto
#killall gunicorn
gunicorn service2.wsgi:application --bind 186.64.122.137:8600

exit
