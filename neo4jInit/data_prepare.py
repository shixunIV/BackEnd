import os
import json
from gpt import GPT, read_config
import concurrent.futures


def process_data(i, data):
    ans = gpt.ask(
        "这是 列车组/乘客/环境/设备 造成的事故?"
        + json.dumps(data[i], ensure_ascii=False)
        + "你只需要回答列车组/乘客/环境/设备即可"
    )
    save_path = os.path.join("neo4jInit/data/new_data", f"railway_{i}.json")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    data[i]["列车组/乘客/环境/设备"] = ans[:2]
    json.dump(
        data[i], open(save_path, "w", encoding="utf-8"), ensure_ascii=False, indent=4
    )


if __name__ == "__main__":
    data = json.load(open("neo4jInit/data/railway.json", encoding="utf-8-sig"))
    config = read_config("./config.yml")
    gpt = GPT(config)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(process_data, range(len(data)), [data] * len(data))
