# 通过main.py一键启动所有服务
import os
import sys


import subprocess


def start_web():
    subprocess.Popen("cd Web && npm i && npm run serve", shell=True)


def start_gateway():
    subprocess.Popen("cd gateway && go mod tidy && go run main.go", shell=True)


def start_neo4j():
    subprocess.Popen("cd neo4j && python main.py", shell=True)


if __name__ == "__main__":
    start_web()
    start_gateway()
    start_neo4j()
