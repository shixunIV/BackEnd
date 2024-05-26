from py2neo import Graph, Node, Relationship
from utils.gpt import GPT, read_config
import re
from datetime import datetime


class Neo4j:
    def __init__(self, config):
        self.config = config
        self.port = config["neo4j"]["port"]
        self.user = config["neo4j"]["user"]
        self.password = config["neo4j"]["password"]
        self.g = Graph(
            host="127.0.0.1",
            port=config["neo4j"]["port"],
            user=config["neo4j"]["user"],
            password=str(config["neo4j"]["password"]),
        )
        self.GPT = GPT(config)

    def run(self, query):
        ans = self.g.run(query)
        res = []
        for i in ans:
            res.append(i)

        return res

    def insert_data_danger(self, data):
        node = Node(
            "hidden_danger",
            id=data["隐患编号"],
            troubleshooting_item_point=data["排查项点（风险点）"],
            troubleshooting_content=data["排查内容（危险源）"],
            troubleshooting_description=data["隐患描述"],
            inspection_time=data["排查时间"],
            place=data["隐患地点"],
        )
        self.g.create(node)
        # 隐患等级如果没有就创建
        node2 = self.g.nodes.match("hidden_danger_level", name=data["隐患等级"]).first()
        if not node2:
            node2 = Node("hidden_danger_level", name=data["隐患等级"])
            self.g.create(node2)
        node3 = self.g.nodes.match(
            "hidden_danger_classification", name=data["隐患分类"]
        ).first()
        if not node3:
            node3 = Node("hidden_danger_classification", name=data["隐患分类"])
            self.g.create(node3)
        node4 = self.g.nodes.match(
            "hidden_danger_source", name=data["隐患来源"]
        ).first()
        if not node4:
            node4 = Node("hidden_danger_source", name=data["隐患来源"])
            self.g.create(node4)
        node5 = self.g.nodes.match("hidden_danger_type", name=data["隐患类型"]).first()
        if not node5:
            node5 = Node("hidden_danger_type", name=data["隐患类型"])
            self.g.create(node5)
        self.g.create(Relationship(node, "hidden_danger_level", node2))
        self.g.create(Relationship(node, "hidden_danger_classification", node3))
        self.g.create(Relationship(node, "hidden_danger_source", node4))
        self.g.create(Relationship(node, "hidden_danger_type", node5))

    def insert_data_accident(self, data):
        result = self.run("MATCH (n:accident) RETURN max(n.index) as max_index")
        max_index = result[0]["max_index"]
        node = Node(
            "accident",
            index=max_index + 1,
            death_toll=int(re.search(r"\d+", data["死亡人数"]).group()),
            injured_toll=int(re.search(r"\d+", data["受伤人数"]).group()),
            detail_reasion=data["原因"],
        )
        self.g.create(node)

        date = datetime.strptime(data["日期"], "%Y年%m月%d日").date()
        time_node = self.run(f"MATCH (n:time) WHERE n.name='{date}' RETURN n")
        if not time_node:
            node = Node("time", name=date)
            self.g.create(node)

        route = self.run(f"MATCH (n:route) WHERE n.name='{data['路线']}' RETURN n")
        if not route:
            node = Node("route", name=data["路线"])
            self.g.create(node)

        place = self.run(f"MATCH (n:place) WHERE n.name='{data['地点']}' RETURN n")
        if not place:
            node = Node("place", name=data["地点"])
            self.g.create(node)

        checi = self.run(f"MATCH (n:checi) WHERE n.name='{data['车次']}' RETURN n")
        if not checi:
            node = Node("checi", name=data["车次"])
            self.g.create(node)

        accident_type = self.run(
            f"MATCH (n:accident_type) WHERE n.name='{data['事故类型']}' RETURN n"
        )
        if not accident_type:
            node = Node("accident_type", name=data["事故类型"])
            self.g.create(node)

        detail_reason = self.run(
            f"MATCH (n:detail_reason) WHERE n.name='{data['原因']}' RETURN n"
        )
        if not detail_reason:
            node = Node("detail_reason", name=data["原因"])
            self.g.create(node)

        self.g.run(
            f"MATCH (a:accident), (b:time) WHERE a.index={max_index + 1} AND b.name='{date}' CREATE (a)-[:occurrence_time]->(b),(b)-[:accident_happen]->(a)"
        )

        self.g.run(
            f"MATCH (a:accident), (b:route) WHERE a.index={max_index + 1} AND b.name='{data['路线']}' CREATE (a)-[:occurrence_route]->(b),(b)-[:accident_happen]->(a)"
        )

        self.g.run(
            f"MATCH (a:accident), (b:place) WHERE a.index={max_index + 1} AND b.name='{data['地点']}' CREATE (a)-[:occurrence_place]->(b),(b)-[:accident_happen]->(a)"
        )

        self.g.run(
            f"MATCH (a:accident), (b:checi) WHERE a.index={max_index + 1} AND b.name='{data['车次']}' CREATE (a)-[:occurrence_train_number]->(b),(b)-[:accident_happen]->(a)"
        )

        self.g.run(
            f"MATCH (a:accident), (b:accident_type) WHERE a.index={max_index + 1} AND b.name='{data['事故类型']}' CREATE (a)-[:occurrence_accident_type]->(b), (b)-[:accident_happen]->(a)"
        )

        self.g.run(
            f"MATCH (a:accident), (b:reason_type) WHERE a.index={max_index + 1} AND b.name='{data['列车组/乘客/环境/设备']}' CREATE (a)-[:occurrence_reason_type]->(b), (b)-[:accident_happen]->(a)"
        )

        return "插入成功！"

    def ask_neo4j_accident(self, question):
        sql = self.GPT.generate_sql_accident(question)
        ans = self.run(sql)
        if ans != "出错啦！":
            return self.GPT.generate_ans_accident(question, ans)
        else:
            return "数据库并没有查询到哦"

    def ask_neo4j_danger(self, question):
        sql = self.GPT.generate_sql_danger(question)
        ans = self.run(sql)
        if ans != "出错啦！":
            return self.GPT.generate_ans_danger(question, ans)
        else:
            return "数据库并没有查询到哦"


if __name__ == "__main__":
    config = read_config("./config.yml")
    neo4j = Neo4j(config)
    print(neo4j.ask_neo4j_accident("哪些事故的是因为乘客造成的?"))
