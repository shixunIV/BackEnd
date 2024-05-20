from flask import Blueprint, request, Response
import json
from utils.neo4j import Neo4j
from utils.config import read_config
from middleware.jwt import jwt_auth

# 创建 Blueprint
accident_api = Blueprint("accident_api", __name__, url_prefix="/api/neo4j/accident")

# 初始化 Neo4j
config = read_config("../config.yml")
neo4j = Neo4j(config)


@accident_api.route("/", methods=["GET"])
@jwt_auth
def ask_question():
    question = request.args.get("question", default="", type=str)
    ans = neo4j.ask_neo4j_accident(question)
    response = Response(
        json.dumps({"answer": ans}, ensure_ascii=False), mimetype="application/json"
    )
    return response


@accident_api.route("/", methods=["POST"])
@jwt_auth
def insert_data():
    data = request.json
    ans = neo4j.insert_data_accident(data)
    response = Response(
        json.dumps({"answer": ans}, ensure_ascii=False), mimetype="application/json"
    )
    return response


@accident_api.route("/list", methods=["GET"])
@jwt_auth
def get_lists():
    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=10, type=int)
    ans = neo4j.run(
        f"MATCH (n:accident) RETURN n SKIP {page_size * (page - 1)} LIMIT {page_size}"
    )
    response = Response(
        json.dumps({"answer": ans}, ensure_ascii=False), mimetype="application/json"
    )
    return response


@accident_api.route("/", methods=["DELETE"])
@jwt_auth
def delete_data():
    index = request.args.get("index", default=0, type=int)
    ans = neo4j.run(f"MATCH (n:accident) WHERE n.index={index} DETACH DELETE n")
    response = Response(
        json.dumps({"answer": ans}, ensure_ascii=False), mimetype="application/json"
    )
    return response


@accident_api.route("/", methods=["PUT"])
@jwt_auth
def update_data():
    data = request.json
    index = data["index"]
    ans = neo4j.run(
        f"MATCH (n:accident) WHERE n.index={index} SET n.death_toll={data['death_toll']},n.injured_toll={data['injured_toll']},n.detail_reason='{data['detail_reason']}'"
    )
    response = Response(
        json.dumps({"answer": ans}, ensure_ascii=False), mimetype="application/json"
    )
    return response
