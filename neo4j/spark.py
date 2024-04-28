from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

SPARKAI_URL = "wss://spark-api.xf-yun.com/v3.5/chat"
SPARKAI_APP_ID = "fbc7bd6f"
SPARKAI_API_SECRET = "ZWI4N2Q5M2NlZDQ3YzFmMzM4YmY0MGVk"
SPARKAI_API_KEY = "f81f4915c4d8fddaafe5a5755fcc0708"
SPARKAI_DOMAIN = "generalv3.5"


question = """
你现在是一个neo4j数据库大师
现在我有一个neo4j数据库，下面列出了该数据库的所有字段，注意这些字段你不需要翻译为英文：
# 所有实体结构：
"疾病"：[名称 描述 是否医保 患病比例 易感人群 治疗周期 治愈率 治疗费用 疾病小贴士 原因 预防 具体表现]
"食物":[名称]
"常用药品":[名称]
"药品明细":[药品明细]
"分类":[名称]
"就诊科室": [名称]
"治疗方式":[名称]
"症状":[名称]
"检查方式";:[名称]
"传染方式",:[名称]
# 关系
[疾病 属于 分类]
[疾病 就诊科室 就诊科室]
[疾病 治疗方式 治疗方式]
[疾病 传染方式 传染方式]
[疾病 症状 症状]
[疾病 检查 检查方式]
[疾病 饮食保健 食物]
[疾病 忌吃食物 食物]
[疾病 推荐食物 食物]
[疾病 常用药品 常用药品]
[疾病 药品明细 药品明细]
[疾病 并发症 疾病]
# 要求
请你根据我的需求给出对应的neo4j查询语句
"""

if __name__ == "__main__":
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )

    messages = [
        ChatMessage(role="user", content=question),
    ]
    while True:
        handler = ChunkPrintHandler()
        a = spark.generate([messages], callbacks=[handler])
        b = a.generations[0][0].text
        messages.append(ChatMessage(role="chat", content=b))
        print(b)
        user_input = input("请输入你的消息：")
        messages.append(ChatMessage(role="user", content=user_input))
