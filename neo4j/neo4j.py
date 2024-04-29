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
        return GPT.generate_ans("阳痿吃什么", neo4j.run(GPT.generate_sql("阳痿吃什么")))


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
