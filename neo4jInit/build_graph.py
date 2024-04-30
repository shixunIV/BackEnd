import json
from py2neo import Graph, Node
import os
import yaml


def read_config(file_path):
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

    def create_diseases(self):
        path = "./neo4jInit/data/new_data"
        # 遍历这个文件夹
        for file in os.listdir(path):
            json_data = json.load(open(os.path.join(path, file), "r", encoding="utf-8"))
            # 疾病节点的属性有 名称，描述，是否医保，患病比例，易感人群,治疗周期,治愈率,治疗费用,推荐,原因,预防,具体表现
            self.g.create(
                Node(
                    "illness",
                    name=json_data["名称"],
                    desc=json_data["描述"][0],
                    medical_insurance=json_data["是否医保"],
                    disease_proportion=json_data["患病比例"],
                    susceptible_population=json_data["易感人群"],
                    treatment_cycle=json_data["治疗周期"],
                    cure_rate=json_data["治愈率"],
                    treatment_cost=json_data["治疗费用"],
                    disease_tips=json_data["推荐"],
                    reason=json_data["原因"],
                    prevention=json_data["预防"],
                    concrete_performance=json_data["具体表现"][0],
                )
            )

    def create_food(self):
        path = "./neo4jInit/data/new_data"
        set_food = set()
        # 遍历这个文件夹
        for file in os.listdir(path):
            json_data = json.load(open(os.path.join(path, file), "r", encoding="utf-8"))
            # 食物节点的属性有 饮食保健，忌吃食物，推荐食物,添加到set_food中
            for tag in ["饮食保健", "忌吃食物", "推荐食物"]:
                for food in json_data[tag]:
                    set_food.add(food)

        for food in set_food:
            self.g.create(Node("food", name=food))

    def create_drug(self):
        path = "./neo4jInit/data/new_data"
        set_drug_常用 = set()
        set_drug_detail = set()
        # 遍历这个文件夹
        for file in os.listdir(path):
            json_data = json.load(open(os.path.join(path, file), "r", encoding="utf-8"))
            # 药品节点的属性有 常用药品，药品明细
            for drug in json_data["常用药品"]:
                set_drug_常用.add(drug)

            for drug in json_data["药品明细"]:
                set_drug_detail.add(drug)

        for drug in set_drug_常用:
            self.g.create(Node("commonly_used_drugs", name=drug))

        for drug in set_drug_detail:
            self.g.create(Node("details_of_drugs", name=drug))

    def create_分类(self):
        path = "./neo4jInit/data/new_data"
        set_分类 = set()
        # 遍历这个文件夹
        for file in os.listdir(path):
            json_data = json.load(open(os.path.join(path, file), "r", encoding="utf-8"))
            for 分类 in json_data["分类"]:
                set_分类.add(分类)

        for tag in set_分类:
            self.g.create(Node("category", name=tag))

    def create_科室(self):
        path = "./neo4jInit/data/new_data"
        set_科室 = set()
        for file in os.listdir(path):
            json_data = json.load(open(os.path.join(path, file), "r", encoding="utf-8"))
            for 就诊科室 in json_data["就诊科室"]:
                set_科室.add(就诊科室)

        for tag in set_科室:
            self.g.create(Node("medical_department", name=tag))

    def create_治疗方式(self):
        path = "./neo4jInit/data/new_data"
        set_治疗方式 = set()
        for file in os.listdir(path):
            json_data = json.load(open(os.path.join(path, file), "r", encoding="utf-8"))
            for 治疗方式 in json_data["治疗方式"]:
                set_治疗方式.add(治疗方式)

        for tag in set_治疗方式:
            self.g.create(Node("treatment_mode", name=tag))

    def create_症状(self):
        path = "./neo4jInit/data/new_data"
        set_症状 = set()
        for file in os.listdir(path):
            json_data = json.load(open(os.path.join(path, file), "r", encoding="utf-8"))
            for 症状 in json_data["症状"]:
                set_症状.add(症状)

        for tag in set_症状:
            self.g.create(Node("symptom", name=tag))

    def create_检查(self):
        path = "./neo4jInit/data/new_data"
        set_检查 = set()
        for file in os.listdir(path):
            json_data = json.load(open(os.path.join(path, file), "r", encoding="utf-8"))
            for 检查 in json_data["检查"]:
                set_检查.add(检查)

        for tag in set_检查:
            self.g.create(Node("inspection_mode", name=tag))

    def create_传染方式(self):
        path = "./neo4jInit/data/new_data"
        set_传染方式 = set()
        for file in os.listdir(path):
            json_data = json.load(open(os.path.join(path, file), "r", encoding="utf-8"))
            for 传染方式 in json_data["传染方式"]:
                set_传染方式.add(传染方式)

        for tag in set_传染方式:
            self.g.create(Node("infection_mode", name=tag))

    def create_entity(self):
        create_methods = [
            self.create_diseases,
            self.create_food,
            self.create_drug,
            self.create_分类,
            self.create_科室,
            self.create_治疗方式,
            self.create_症状,
            self.create_检查,
            self.create_传染方式,
        ]
        for method in create_methods:
            method()

    def create_疾病_to_分类(self):
        path = "./neo4jInit/data/new_data"
        for file in os.listdir(path):
            json_data = json.load(open(os.path.join(path, file), "r", encoding="utf-8"))
            for 分类 in json_data["分类"]:
                self.g.run(
                    "MATCH (a:illness),(b:category) WHERE a.name = $a AND b.name = $b CREATE (a)-[r:belong]->(b)",
                    a=json_data["名称"],
                    b=分类,
                )

    def create_疾病_to_科室(self):
        path = "./neo4jInit/data/new_data"
        for file in os.listdir(path):
            json_data = json.load(open(os.path.join(path, file), "r", encoding="utf-8"))
            for 就诊科室 in json_data["就诊科室"]:
                self.g.run(
                    "MATCH (a:illness),(b:medical_department) WHERE a.name = $a AND b.name = $b CREATE (a)-[r:medical_department]->(b)",
                    a=json_data["名称"],
                    b=就诊科室,
                )

    def create_疾病_to_治疗方式(self):
        path = "./neo4jInit/data/new_data"
        for file in os.listdir(path):
            json_data = json.load(open(os.path.join(path, file), "r", encoding="utf-8"))
            for 治疗方式 in json_data["治疗方式"]:
                self.g.run(
                    "MATCH (a:illness),(b:treatment_mode) WHERE a.name = $a AND b.name = $b CREATE (a)-[r:treatment_mode]->(b)",
                    a=json_data["名称"],
                    b=治疗方式,
                )

    def create_疾病_to_传染方式(self):
        path = "./neo4jInit/data/new_data"
        for file in os.listdir(path):
            json_data = json.load(open(os.path.join(path, file), "r", encoding="utf-8"))
            for 传染方式 in json_data["传染方式"]:
                self.g.run(
                    "MATCH (a:illness),(b:infection_mode) WHERE a.name = $a AND b.name = $b CREATE (a)-[r:infection_mode]->(b)",
                    a=json_data["名称"],
                    b=传染方式,
                )

    def create_疾病_to_症状(self):
        path = "./neo4jInit/data/new_data"
        for file in os.listdir(path):
            json_data = json.load(open(os.path.join(path, file), "r", encoding="utf-8"))
            for 症状 in json_data["症状"]:
                self.g.run(
                    "MATCH (a:illness),(b:symptom) WHERE a.name = $a AND b.name = $b CREATE (a)-[r:symptom]->(b)",
                    a=json_data["名称"],
                    b=症状,
                )

    def create_疾病_to_检查(self):
        path = "./neo4jInit/data/new_data"
        for file in os.listdir(path):
            json_data = json.load(open(os.path.join(path, file), "r", encoding="utf-8"))
            for 检查 in json_data["检查"]:
                self.g.run(
                    "MATCH (a:illness),(b:inspection_mode) WHERE a.name = $a AND b.name = $b CREATE (a)-[r:inspection_mode]->(b)",
                    a=json_data["名称"],
                    b=检查,
                )

    def create_疾病_to_饮食保健(self):
        path = "./neo4jInit/data/new_data"
        for file in os.listdir(path):
            json_data = json.load(open(os.path.join(path, file), "r", encoding="utf-8"))
            for 饮食保健 in json_data["饮食保健"]:
                self.g.run(
                    "MATCH (a:illness),(b:food) WHERE a.name = $a AND b.name = $b CREATE (a)-[r:diet_and_health_care]->(b)",
                    a=json_data["名称"],
                    b=饮食保健,
                )

    def create_疾病_to_忌吃食物(self):
        path = "./neo4jInit/data/new_data"
        for file in os.listdir(path):
            json_data = json.load(open(os.path.join(path, file), "r", encoding="utf-8"))
            for 忌吃食物 in json_data["忌吃食物"]:
                self.g.run(
                    "MATCH (a:illness),(b:food) WHERE a.name = $a AND b.name = $b CREATE (a)-[r:avoid_eating_food]->(b)",
                    a=json_data["名称"],
                    b=忌吃食物,
                )

    def create_疾病_to_推荐食物(self):
        path = "./neo4jInit/data/new_data"
        for file in os.listdir(path):
            json_data = json.load(open(os.path.join(path, file), "r", encoding="utf-8"))
            for 推荐食物 in json_data["推荐食物"]:
                self.g.run(
                    "MATCH (a:illness),(b:food) WHERE a.name = $a AND b.name = $b CREATE (a)-[r:recommend_food]->(b)",
                    a=json_data["名称"],
                    b=推荐食物,
                )

    def create_疾病_to_常用药品(self):
        path = "./neo4jInit/data/new_data"
        for file in os.listdir(path):
            json_data = json.load(open(os.path.join(path, file), "r", encoding="utf-8"))
            for 常用药品 in json_data["常用药品"]:
                self.g.run(
                    "MATCH (a:illness),(b:commonly_used_drugs) WHERE a.name = $a AND b.name = $b CREATE (a)-[r:commonly_used_drugs]->(b)",
                    a=json_data["名称"],
                    b=常用药品,
                )

    def create_疾病_to_药品明细(self):
        path = "./neo4jInit/data/new_data"
        for file in os.listdir(path):
            json_data = json.load(open(os.path.join(path, file), "r", encoding="utf-8"))
            for 药品明细 in json_data["药品明细"]:
                self.g.run(
                    "MATCH (a:illness),(b:details_of_drugs) WHERE a.name = $a AND b.name = $b CREATE (a)-[r:details_of_drugs]->(b)",
                    a=json_data["名称"],
                    b=药品明细,
                )

    def create_疾病_to_并发症(self):
        path = "./neo4jInit/data/new_data"
        for file in os.listdir(path):
            json_data = json.load(open(os.path.join(path, file), "r", encoding="utf-8"))
            for 并发症 in json_data["并发症"]:
                self.g.run(
                    "MATCH (a:illness),(b:illness) WHERE a.name = $a AND b.name = $b CREATE (a)-[r:complication]->(b)",
                    a=json_data["名称"],
                    b=并发症,
                )

    def create_association(self):
        create_methods = [
            self.create_疾病_to_分类,
            self.create_疾病_to_科室,
            self.create_疾病_to_治疗方式,
            self.create_疾病_to_传染方式,
            self.create_疾病_to_症状,
            self.create_疾病_to_检查,
            self.create_疾病_to_饮食保健,
            self.create_疾病_to_忌吃食物,
            self.create_疾病_to_推荐食物,
            self.create_疾病_to_常用药品,
            self.create_疾病_to_药品明细,
            self.create_疾病_to_并发症,
        ]
        for method in create_methods:
            method()


if __name__ == "__main__":
    handler = MedicalGraph()
    handler.create_entity()
    handler.create_association()
