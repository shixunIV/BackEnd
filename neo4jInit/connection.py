import json
from py2neo import Graph, Node
import os
import yaml
from py2neo import Relationship
from datetime import datetime
import re
import pandas as pd


def read_config(file_path):
    with open(file_path, "r") as file:
        config_data = yaml.safe_load(file)
    return config_data


class MedicalGraph:
    def __init__(self):
        config = read_config("../config.yml")
        self.g = Graph(
            host="127.0.0.1",
            port=config["neo4j"]["port"],
            user=config["neo4j"]["user"],
            password=str(config["neo4j"]["password"]),
        )
        self.data = self.read_csv()
        self.excel = self.read_excel()

    def read_csv(self):
        path = "./data/output.txt"
        data = []
        with open(path, "r", encoding="utf-8") as f:
            # 逐行读取并且按照||分割
            for line in f.readlines():
                line = line.strip().split("||")
                # print(line)
                data.append(line)
        return data

    def read_excel(self):
        path = "./data/隐患库.xlsx"
        pf = pd.read_excel(path, sheet_name=0)
        data = pf.values
        # 按照data[2]作为字典的key
        maps = {}
        for i in range(len(data)):
            maps[data[i][8]] = data[i]
        return maps

    def build(self):
        for i in range(len(self.data)):
            accident_index = int(self.data[i][0]) + 1
            reason = self.data[i][2]
            target = self.excel.get(reason)
            hidden_danger_index = target[3]
            gailv = float(self.data[i][-1])
            hidden_danger = self.g.nodes.match(
                "hidden_danger", id=hidden_danger_index
            ).first()
            accident = self.g.nodes.match("accident", index=accident_index).first()
            # 创建链接
            if hidden_danger is not None and accident is not None:
                relation = Relationship(
                    accident, "hidden_danger", hidden_danger, probability=gailv
                )
                self.g.create(relation)
                print("创建关系成功")


if __name__ == "__main__":
    medical = MedicalGraph()
    medical.build()
