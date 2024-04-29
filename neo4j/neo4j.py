from py2neo import Graph, Node
from gpt import GPT


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

    def ask_neo4j(self, question):
        ans = self.run(self.GPT.generate_sql(question))
        if ans != "出错啦！":
            return self.GPT.generate_ans(question, ans)
        else:
            return "数据库并没有查询到哦"


if __name__ == "__main__":
    config = {
        "neo4j": {
            "port": 7687,
            "user": "neo4j",
            "password": "12345678",
        }
    }
    neo4j = Neo4j(config)
    print(neo4j.ask_neo4j("阳痿吃什么"))
