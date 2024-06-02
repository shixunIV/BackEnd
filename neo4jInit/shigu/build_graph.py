import json
from py2neo import Graph, Node
import os
import yaml
from py2neo import Relationship
from datetime import datetime
import re


def read_config(file_path):
    with open(file_path, "r") as file:
        config_data = yaml.safe_load(file)
    return config_data


class MedicalGraph:
    def __init__(self):
        self.data_path = "./neo4jInit/data/new_data"
        self.data = self.read_nodes()
        config = read_config("config.yml")
        self.g = Graph(
            host="127.0.0.1",
            port=config["neo4j"]["port"],
            user=config["neo4j"]["user"],
            password=str(config["neo4j"]["password"]),
        )

    def read_nodes(self):
        data = []
        for file in os.listdir(self.data_path):
            with open(os.path.join(self.data_path, file), "r", encoding="utf-8") as f:
                data.append(json.load(f))
        return data

    def create_time_node(self):
        time = set()
        for item in self.data:
            time.add(item["日期"])
        for item in time:
            # 尝试使用第一种格式解析日期
            try:
                date = datetime.strptime(item, "%Y年%m月%d日").date()
            except ValueError:
                # 如果第一种格式失败，尝试使用第二种格式
                try:
                    date = datetime.strptime(item, "%Y年%m月%d日%H时%M分").date()
                except ValueError:
                    print(f"无法解析日期: {item}")
                    continue
            node = Node("time", name=date)
            self.g.create(node)

    def create_route_node(self):
        road = set()
        for item in self.data:
            road.add(item["路线"])
        for item in road:
            node = Node("route", name=item)
            self.g.create(node)

    def create_place_node(self):
        place = set()
        for item in self.data:
            place.add(item["地点"])
        for item in place:
            node = Node("place", name=item)
            self.g.create(node)

    def create_checi_node(self):
        checi = set()
        for item in self.data:
            checi.add(item["车次"])
        for item in checi:
            node = Node("train_number", name=item)
            self.g.create(node)

    def create_事故类型_node(self):
        accident_type = set()
        for item in self.data:
            accident_type.add(item["事故类型"])
        for item in accident_type:
            node = Node("accident_type", name=item)
            self.g.create(node)

    def create_详细原因_node(self):
        detail_reason = set()
        for item in self.data:
            detail_reason.add(item["原因"])
        for item in detail_reason:
            node = Node("detail_reason", name=item)
            self.g.create(node)

    def create_原因类型_node(self):
        reason_type = set()
        for item in self.data:
            reason_type.add(item["列车组/乘客/环境/设备"])
        for item in reason_type:
            node = Node("reason_type", name=item)
            self.g.create(node)

    def create_Main_node(self):
        i = 0
        for item in self.data:
            i += 1
            node = Node(
                "accident",
                index=i,
                death_toll=int(re.search(r"\d+", item["死亡人数"]).group()),
                injured_toll=int(re.search(r"\d+", item["受伤人数"]).group()),
                detail_reason=item["原因"],
            )
            self.g.create(node)

    def create_entity(self):
        create_methods = [
            self.create_time_node,
            self.create_route_node,
            self.create_place_node,
            self.create_checi_node,
            self.create_事故类型_node,
            self.create_详细原因_node,
            self.create_原因类型_node,
            self.create_Main_node,
        ]
        for method in create_methods:
            method()

    def create_time_relation(self):
        i = 0
        for item in self.data:
            i += 1
            try:
                date = datetime.strptime(item["日期"], "%Y年%m月%d日").date()
            except ValueError:
                # 如果第一种格式失败，尝试使用第二种格式
                try:
                    date = datetime.strptime(
                        item["日期"], "%Y年%m月%d日%H时%M分"
                    ).date()
                except ValueError:
                    print(f"无法解析日期: {item}")
                    continue
            node1 = self.g.nodes.match("time", name=date).first()
            node2 = self.g.nodes.match("accident", index=i).first()
            relation = Relationship(node2, "occurrence_time", node1)
            self.g.create(relation)
            relation = Relationship(node1, "accident_happen", node2)
            self.g.create(relation)

    def create_route_relation(self):
        i = 0
        for item in self.data:
            i += 1
            node1 = self.g.nodes.match("route", name=item["路线"]).first()
            node2 = self.g.nodes.match("accident", index=i).first()
            relation = Relationship(node2, "occurrence_route", node1)
            self.g.create(relation)
            relation = Relationship(node1, "accident_happen", node2)
            self.g.create(relation)

    def create_place_relation(self):
        i = 0
        for item in self.data:
            i += 1
            node1 = self.g.nodes.match("place", name=item["地点"]).first()
            node2 = self.g.nodes.match("accident", index=i).first()
            relation = Relationship(node2, "occurrence_place", node1)
            self.g.create(relation)
            relation = Relationship(node1, "accident_happen", node2)
            self.g.create(relation)

    def create_checi_relation(self):
        i = 0
        for item in self.data:
            i += 1
            node1 = self.g.nodes.match("train_number", name=item["车次"]).first()
            node2 = self.g.nodes.match("accident", index=i).first()
            relation = Relationship(node2, "occurrence_train_number", node1)
            self.g.create(relation)
            relation = Relationship(node1, "accident_happen", node2)
            self.g.create(relation)

    def create_事故类型_relation(self):
        i = 0
        for item in self.data:
            i += 1
            node1 = self.g.nodes.match("accident_type", name=item["事故类型"]).first()
            node2 = self.g.nodes.match("accident", index=i).first()
            relation = Relationship(node2, "occurrence_accident_type", node1)
            self.g.create(relation)
            relation = Relationship(node1, "accident_happen", node2)
            self.g.create(relation)

    def create_原因类型_relation(self):
        i = 0
        for item in self.data:
            i += 1
            node1 = self.g.nodes.match(
                "reason_type", name=item["列车组/乘客/环境/设备"]
            ).first()
            node2 = self.g.nodes.match("accident", index=i).first()
            relation = Relationship(node2, "occurrence_reason_type", node1)
            self.g.create(relation)
            relation = Relationship(node1, "accident_happen", node2)
            self.g.create(relation)

    def create_association(self):
        create_methods = [
            self.create_time_relation,
            self.create_route_relation,
            self.create_place_relation,
            self.create_checi_relation,
            self.create_事故类型_relation,
            self.create_原因类型_relation,
        ]
        for method in create_methods:
            method()


if __name__ == "__main__":
    handler = MedicalGraph()
    handler.create_entity()
    handler.create_association()
