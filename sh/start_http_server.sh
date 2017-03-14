#!/bin/bash
# redis_start.sh

# 切换虚拟环境
source $HOME/.bash_profile
workon bpsg

if [ -f ../tmp/bs2Http.pid ]
then
    kill `cat ../tmp/bs2Http.pid`
fi

cd ../
twistd --pidfile=../tmp/bs2Http.pid bs2err --port 7777


