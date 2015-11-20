#!/bin/bash

# -*- ENCODING: UTF-8 -*-
#echo "Introduce tu puerto : "
#read puerto
sudo sync
sudo sysctl -w vm.drop_caches=3
sudo sync
sync && echo 3 > /proc/sys/vm/drop_caches

exit