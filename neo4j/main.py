from flask import Flask, request, jsonify
import json
import os
import yaml
from py2neo import Graph, Node
from neo4j import Neo4j


def read_config(file_path):
    if not os.path.exists(file_path):
        # 创建这个文件并且写入初始化代码
        with open(file_path, "w") as file:
            file.write("neo4j:\n")
            file.write("  port: 7687\n")
            file.write("  user: neo4j\n")
            file.write("  password: 12345678\n")
            file.flush()
    with open(file_path, "r") as file:
        config_data = yaml.safe_load(file)
    return config_data


app = Flask(__name__)
config = read_config("../config.yml")
neo4j = Neo4j(config)


@app.route("/api/neo4j", methods=["GET"])
def ask_question():
    question = request.args.get("question", default="", type=str)
    print(question)
    ans = "你好"
    return jsonify({"answer": ans})


if __name__ == "__main__":
    app.run(port=9001)
