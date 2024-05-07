from flask import Flask, request, jsonify, Response
import yaml
from neo4j import Neo4j
import json


def read_config(file_path):
    with open(file_path, "r") as file:
        config_data = yaml.safe_load(file)
    return config_data


app = Flask(__name__)
config = read_config("../config.yml")
neo4j = Neo4j(config)


@app.route("/api/neo4j", methods=["GET"])
def ask_question():
    question = request.args.get("question", default="", type=str)
    ans = neo4j.ask_neo4j(question)
    response = Response(
        json.dumps({"answer": ans}, ensure_ascii=False), mimetype="application/json"
    )
    return response


@app.route("/api/neo4j", methods=["POST"])
def insert_data():
    data = request.json
    ans = neo4j.insert_data(data)
    response = Response(
        json.dumps({"answer": ans}, ensure_ascii=False), mimetype="application/json"
    )
    return response


if __name__ == "__main__":
    app.run(port=9002)
