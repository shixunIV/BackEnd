import os
import json
import jieba
import concurrent.futures


def process_file(i):
    path = "./neo4jInit/data/spider_data"
    target_path = "./neo4jInit/data/new_data/"
    # 载入path
    with open(os.path.join(path, str(i) + ".json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    # 需要的数据
    dict = {}
    dict["名称"] = data["basic_info"]["name"]
    dict["描述"] = data["basic_info"]["desc"]
    dict["分类"] = data["basic_info"]["category"][1:-1]
    dict["是否医保"] = (
        data["basic_info"]["attributes"][0].split("：")[1].replace(" ", "")
    )
    dict["患病比例"] = data["basic_info"]["attributes"][1].split("：")[1]
    dict["易感人群"] = (
        data["basic_info"]["attributes"][2].split("：")[1].replace(" ", "")
    )
    dict["传染方式"] = data["basic_info"]["attributes"][3].split("：")[1]
    sym = data["basic_info"]["attributes"][4].split("：")[1]
    words = jieba.lcut(sym)
    dict["并发症"] = words
    seg_list = jieba.lcut(
        data["basic_info"]["attributes"][5].split("：")[1], cut_all=False
    )
    seg_list = [x for x in seg_list if x != " "]
    dict["就诊科室"] = seg_list
    dict["治疗方式"] = data["basic_info"]["attributes"][6].split("：")[1].split(" ")
    dict["治疗周期"] = data["basic_info"]["attributes"][7].split("：")[1]
    dict["治愈率"] = data["basic_info"]["attributes"][8].split("：")[1].replace(" ", "")
    dict["治疗费用"] = data["basic_info"]["attributes"][9].split("：")[1]
    dict["推荐"] = data["basic_info"]["attributes"][10]
    dict["原因"] = data["cause_info"]
    dict["预防"] = data["prevent_info"]
    dict["症状"] = data["symptom_info"][0]
    dict["具体表现"] = data["symptom_info"][1]
    dict["检查"] = data["inspect_info"]
    dict["饮食保健"] = data["food_info"]["good"]
    dict["忌吃食物"] = data["food_info"]["bad"]
    dict["推荐食物"] = data["food_info"]["recommand"]
    dict["常用药品"] = data["common_drug"]
    dict["药品明细"] = data["drug_detail"]
    save_path = os.path.join(target_path, str(i) + ".json")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(dict, f, ensure_ascii=False, indent=4)


def prepare_data():
    path = "./neo4jInit/data/disease.txt"
    with open(path, "r", encoding="utf-8") as f:
        sympotom = [line.strip() for line in f]
    jieba.load_userdict(sympotom)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_file, range(1, 10138))


def get_entity():
    dict = {}
    dict["名称"] = set()
    dict["分类"] = set()  # 去掉第一个疾病百科和最后一个重复名称
    dict["就诊科室"] = set()
    dict["治疗方式"] = set()
    dict["传染方式"] = set()
    dict["症状"] = set()
    dict["检查"] = set()
    dict["食物"] = set()
    dict["药品"] = set()
    dict["细分药品"] = set()


def create_diseases():
    path = "./neo4jInit/data/new_data"
    # 遍历这个文件夹
    for file in os.listdir(path):
        json_data = json.load(open(os.path.join(path, file), "r", encoding="utf-8"))
        # 节点的属性有 名称，描述，是否医保，患病比例，易感人群


if __name__ == "__main__":
    prepare_data()
    # create_diseases()
