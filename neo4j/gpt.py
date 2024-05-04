from openai import OpenAI
import re
import yaml

# TODO!待修改的提示词
prompt ="""你现在是一个neo4j数据库查询高手,现在有一个铁路事故图数据库
# 所有实体结构([]中的是字段解释)：
```python
Node("time", name["事故事件"])

Node("route", name["事故路线"])

Node("place", name["事故地点"])

Node("train_number", name["事故车次"])

Node("accident_type", name["事故类型,比如山洪地震"])

Node("detail_reason", name["事故详细原因"])

Node("reason_type", name["事故原因分类,是乘务组原因还是环境还是乘客导致"])

Node(
	"accident",
	index["事故索引"],
	death_toll["死亡人数"],
	injured_toll["受伤人数"],
)
```
# 关系三元组
[accident occurrence_time time]
[ accident occurrence_route route]
[accident occurrence_place place]
[accident occurrence_train_number train_number]
[accident occurrence_accident_type accident_type]
[accident occurrence_detail_reason detail_reason]
[accident occurrence_reason_type reason_type]
# 要求
请你根据我接下来的问题给出对应的neo4j查询语句，neo4j语句需包含在```cypher```代码块中
"""


def read_config(file_path):
    with open(file_path, "r") as file:
        config_data = yaml.safe_load(file)
    return config_data


class GPT:
    def __init__(self, config) -> None:
        self.client = OpenAI(
            api_key=config["openai"]["api_key"],
        )

    def generate_sql(self, question):
        global prompt
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
                {
                    "role": "assistant",
                    "content": """
    Sure, I can help you with that. Just let me know what specific queries you need for Neo4j, and I'll provide you with the corresponding Cypher queries.""",
                },
                {
                    "role": "user",
                    "content": question,
                },
            ],
        )
        # 使用正则匹配出cypher语句
        pattern = r"```cypher(.*?)```"
        match = re.search(
            pattern, response.choices[0].message.content.strip(), re.DOTALL
        )
        if match:
            cypher_query = match.group(1).strip()
            return cypher_query
        else:
            return "出错啦！"

    def generate_ans(self, question, ans):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": "你现在是一个医生，请你根据我的问题和根据该问题从数据库中查询出来的结果组织成人类语言返回",
                },
                {
                    "role": "assistant",
                    "content": "当然，请问你有什么健康问题需要咨询？",
                },
                {
                    "role": "user",
                    "content": f"问题:{question}  查询结果{ans}",
                },
            ],
        )
        print(f"问题:{question}  查询结果{ans}")  #
        return response.choices[0].message.content.strip()

    def ask(self, question):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": question,
                },
            ],
        )
        print(f"问题:{question}  查询结果{response.choices[0].message.content.strip()}")


if __name__ == "__main__":
    config = read_config("./config.yml")
    gpt = GPT(config)
    # print(gpt.generate_sql("阳痿吃什么"))
    gpt.ask("阳痿吃什么")