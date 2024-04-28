from py2neo import Graph, Node


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

    def run(self, query):
        return self.g.run(query)
