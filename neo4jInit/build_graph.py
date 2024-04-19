import os
import json
from py2neo import Graph, Node
import yaml


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


class MedicalGraph:
    def __init__(self):
        self.data_path = "./neo4jInit/data/medical.json"
        config = read_config("config.yml")
        self.g = Graph(
            host="127.0.0.1",
            port=config["neo4j"]["port"],
            user=config["neo4j"]["user"],
            password=str(config["neo4j"]["password"]),
        )

    def read_data(self):
        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
