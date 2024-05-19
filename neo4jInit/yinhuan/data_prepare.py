import pandas as pd
from py2neo import Graph, Node,Relationship
from datetime import datetime
# 读取数据
data = pd.read_excel('./neo4jInit/data/隐患库.xlsx', sheet_name=0)
# 需要的列有：排查时间 排查部门 隐患编号 隐患等级 排查项点（风险点） 排查内容（危险源） 隐患描述 隐患分类 隐患类型 隐患地点
data = data[['排查时间', '排查部门', '隐患编号',"隐患来源", '隐患等级', '排查项点（风险点）', '排查内容（危险源）', '隐患描述', '隐患分类', '隐患类型', '隐患地点']]
# 排查时间转为2023-07-14的格式
g = Graph(
        host="127.0.0.1",
        port=7687,
        user='neo4j',
        password='12345678',
    )
# 隐患编号 排查项点（风险点） 排查内容（危险源） 隐患描述 是自己的属性,创建节点,时间的结构如下：2023-07-13 20:11
for index, row in data.iterrows():
    node = Node("hidden_danger",id=row['隐患编号'],troubleshooting_item_point=row['排查项点（风险点）'],troubleshooting_content=row['排查内容（危险源）'],troubleshooting_description=row['隐患描述'],inspection_time=row['排查时间'],place=row['隐患地点'])
    g.create(node)

隐患等级 = set(data['隐患等级'])
隐患分类 = set(data['隐患分类'])
隐患来源 = set(data['隐患来源'])
隐患类型 = set(data['隐患类型'])
for item in 隐患等级:
    node = Node("hidden_danger_level",name=item)
    g.create(node)

for item in 隐患分类:
    node = Node("hidden_danger_classification",name=item)
    g.create(node)

for item in 隐患来源:
    node = Node("hidden_danger_source",name=item)
    g.create(node)

for item in 隐患类型:
    node = Node("hidden_danger_type",name=item)
    g.create(node)


# 创建关系
for index, row in data.iterrows():
    node1 = g.nodes.match("hidden_danger",id=row['隐患编号']).first()
    node2 = g.nodes.match("hidden_danger_level",name=row['隐患等级']).first()
    node3 = g.nodes.match("hidden_danger_classification",name=row['隐患分类']).first()
    node4 = g.nodes.match("hidden_danger_source",name=row['隐患来源']).first()
    node5 = g.nodes.match("hidden_danger_type",name=row['隐患类型']).first()
    g.create(Relationship(node1, "hidden_danger_level", node2))
    g.create(Relationship(node1, "hidden_danger_classification", node3))
    g.create(Relationship(node1, "hidden_danger_source", node4))
    g.create(Relationship(node1, "hidden_danger_type", node5))

 