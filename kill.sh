#!/bin/bash

# 杀死9000~9002端口上的程序
for port in {9000..9002}
do
    echo "Checking port $port"
    pid=$(lsof -t -i:$port)
    if [ -n "$pid" ]; then
        echo "Killing process on port $port with PID $pid"
        kill -9 $pid
    else
        echo "No process running on port $port"
    fi
done