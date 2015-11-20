#!/bin/bash

# -*- ENCODING: UTF-8 -*-
#echo "Introduce tu puerto : "
#read puerto
#killall celery
export C_FORCE_ROOT="true"
celery -A bluecategory worker -l info

exit