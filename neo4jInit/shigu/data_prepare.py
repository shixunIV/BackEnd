import os
import json
import concurrent.futures
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

# 星火认知大模型v3.5的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = "wss://spark-api.xf-yun.com/v3.5/chat"
# 星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
SPARKAI_APP_ID = "fbc7bd6f"
SPARKAI_API_KEY = "f81f4915c4d8fddaafe5a5755fcc0708"
SPARKAI_API_SECRET = "ZWI4N2Q5M2NlZDQ3YzFmMzM4YmY0MGVk"
# 星火认知大模型v3.5的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = "generalv3.5"


def process_data(i, data):
    try:
        if os.path.exists(os.path.join("neo4jInit/data/new_data", f"railway_{i}.json")):
            return
        spark = ChatSparkLLM(
            spark_api_url=SPARKAI_URL,
            spark_app_id=SPARKAI_APP_ID,
            spark_api_key=SPARKAI_API_KEY,
            spark_api_secret=SPARKAI_API_SECRET,
            spark_llm_domain=SPARKAI_DOMAIN,
            streaming=False,
        )
        del data[i]["备注"]
        messages = [
            ChatMessage(
                role="user",
                content="这是 列车组/乘客/环境/设备 造成的事故:"
                + json.dumps(data[i], ensure_ascii=False)
                + "\n你只需要回答列车组/乘客/环境/设备即可",
            )
        ]
        handler = ChunkPrintHandler()
        a = spark.generate([messages], callbacks=[handler])
        print(a.generations[0][0].text)
        if "列车组" in a.generations[0][0].text:
            ans = "列车组"
        elif "乘客" in a.generations[0][0].text:
            ans = "乘客"
        elif "环境" in a.generations[0][0].text:
            ans = "环境"
        elif "设备" in a.generations[0][0].text:
            ans = "设备" 
        else:
            ans = "未知"
        data[i]["列车组/乘客/环境/设备"] = ans
        save_path = os.path.join("neo4jInit/data/new_data", f"railway_{i}.json")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        json.dump(
            data[i],
            open(save_path, "w", encoding="utf-8"),
            ensure_ascii=False,
            indent=4,
        )
    except Exception as e:
        return


if __name__ == "__main__":
    data = json.load(open("neo4jInit/data/railway.json", encoding="utf-8-sig"))
    # config = read_config("./config.yml")
    # gpt = GPT(config)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(process_data, range(len(data)), [data] * len(data))
