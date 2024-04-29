from openai import OpenAI
import re
import yaml

prompt = """
你现在是一个neo4j数据库查询高手
# 所有实体结构：
```python
Node(
	"illness",
	name["名称"],
	desc["描述"],
	medical_insurance["是否医保"],
	disease_proportion["患病比例"],
	susceptible_population["易感人群"],
	treatment_cycle["治疗周期"],
	cure_rate["治愈率"],
	treatment_cost["治疗费用"],
	disease_tips["推荐"],
	reason["原因"],
	prevention["预防"],
	concrete_performance["具体表现"],
)

Node("food", name["食品名称"])

Node("commonly_used_drugs", name["药品名称"])

Node("details_of_drugs", name["药品名称"])

Node("category", name["疾病分类"])

Node("medical_department", name["就诊科室"])

Node("treatment_mode", name["治疗方式"]

Node("symptom", name["症状"])	

Node("inspection_mode", name["检查方式"])

Node("infection_mode", name["传染方式"]) 
```
# 关系三元组

[illness belong category]
[illness medical_department medical_department]
[illness treatment_mode treatment_mode]
[illness infection_mode infection_mode]
[illness symptom symptom]
[illness inspection_mode inspection_mode]
[illness diet_and_health_care food]
[illness avoid_eating_food food]
[illness recommend_food food]
[illness commonly_used_drugs commonly_used_drugs]
[illness details_of_drugs details_of_drugs]
[illness compliation illness]
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
        print(f"问题:{question}  查询结果{ans}")
        return response.choices[0].message.content.strip()


if __name__ == "__main__":
    config = read_config("./config.yml")
    gpt = GPT(config)
    print(gpt.generate_sql("阳痿吃什么"))