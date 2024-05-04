from flask import Flask, request, jsonify
import yaml
from neo4j import Neo4j


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
    return jsonify({"answer": ans})


# {
#     "日期": "1950年1月23日",
#     "路线": "津浦",
#     "地点": "南京市花旗营站",
#     "车次": "2404（军用列车）301次旅客列车",
#     "事故类型": "正面相撞",
#     "原因": "扳道工操作失误",
#     "死亡人数": "16",
#     "受伤人数": "46",
#     "列车组/乘客/环境/设备": "列车组"
# }
@app.route("/api/neo4j", methods=["POST"])
def insert_data():
    data = request.json
    ans = neo4j.insert_data(data)
    return jsonify({"answer": ans})


if __name__ == "__main__":
    app.run(port=9002)
