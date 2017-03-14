#!/bin/bash
# redis_start.sh

# 切换虚拟环境
source $HOME/.bash_profile
workon bpsg

cd ../
python http_receive_error.py &
ps -ef | grep http_receive_error.py

