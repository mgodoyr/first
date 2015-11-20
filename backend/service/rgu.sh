#!/bin/bash

# -*- ENCODING: UTF-8 -*-
#echo "Introduce tu puerto : "
#read puerto
#killall gunicorn
gunicorn service.wsgi:application --bind 186.64.122.137:8500

exit
