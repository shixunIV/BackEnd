from flask import Blueprint, request, Response
import json
from utils.neo4j import Neo4j
from utils.config import read_config
from middleware.jwt import jwt_auth
from datetime import datetime

# 创建 Blueprint
hidden_danger_api = Blueprint("hidden_danger", __name__, url_prefix="/api/neo4j/danger")

config = read_config("../config.yml")
neo4j = Neo4j(config)


@hidden_danger_api.route("/", methods=["GET"])
@jwt_auth
def ask_question():
    question = request.args.get("question", default="", type=str)
    ans = neo4j.ask_neo4j_danger(question)
    response = Response(
        json.dumps({"answer": ans}, ensure_ascii=False), mimetype="application/json"
    )
    return response


@hidden_danger_api.route("/list", methods=["GET"])
@jwt_auth
def get_lists():
    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=10, type=int)
    ans = neo4j.run(
        f"MATCH (n:hidden_danger) RETURN n SKIP {page_size * (page - 1)} LIMIT {page_size}"
    )
    print(ans)
    response = Response(
        json.dumps({"answer": ans}, ensure_ascii=False, default=str),
        mimetype="application/json",
    )
    return response


@hidden_danger_api.route("/", methods=["POST"])
@jwt_auth
def insert_data():
    data = request.json
    ans = neo4j.insert_data_danger(data)
    response = Response(
        json.dumps({"answer": ans}, ensure_ascii=False), mimetype="application/json"
    )
    return response


@hidden_danger_api.route("/", methods=["DELETE"])
@jwt_auth
def delete_data():
    id = request.args.get("id", default=0, type=int)
    ans = neo4j.run(f"MATCH (n:hidden_danger) WHERE n.id={id} DETACH DELETE n")
    response = Response(
        json.dumps({"answer": ans}, ensure_ascii=False), mimetype="application/json"
    )
    return response
