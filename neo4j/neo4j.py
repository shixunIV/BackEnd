from py2neo import Graph, Node
from gpt import GPT, read_config
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

    def insert_data(self, data):
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

        # [accident occurrence_time time]
        # [time accident_happen accident]
        # [accident occurrence_route route]
        # [route accident_happen accident]
        # [accident occurrence_place place]
        # [place accident_happen accident]
        # [accident occurrence_train_number train_number]
        # [train_number accident_happen accident]
        # [accident occurrence_accident_type accident_type]
        # [accident_type accident_happen accident]
        # [accident occurrence_reason_type reason_type]
        # [reason_type accident_happen accident]
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

    def ask_neo4j(self, question):
        sql = self.GPT.generate_sql(question)
        ans = self.run(sql)
        if ans != "出错啦！":
            return self.GPT.generate_ans(question, ans)
        else:
            return "数据库并没有查询到哦"


if __name__ == "__main__":
    config = read_config("./config.yml")
    neo4j = Neo4j(config)
    print(neo4j.ask_neo4j("哪些事故的是因为乘客造成的?"))
