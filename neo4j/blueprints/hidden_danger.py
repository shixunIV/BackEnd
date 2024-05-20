from flask import Blueprint, request, Response
import json
from utils.neo4j import Neo4j
from utils.config import read_config 
from middleware.jwt import jwt_auth

# 创建 Blueprint
hidden_danger_api = Blueprint('hidden_danger', __name__, url_prefix='/api/neo4j/danger')

config = read_config("../config.yml")
neo4j = Neo4j(config)

@hidden_danger_api.route("/", methods=["GET"])
@jwt_auth
def ask_question():
    question = request.args.get("question", default="", type=str)
    ans = neo4j.ask_neo4j_accident(question)
    response = Response(
        json.dumps({"answer": ans}, ensure_ascii=False), mimetype="application/json"
    )
    return response