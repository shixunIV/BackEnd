import os
import json
import jieba
import concurrent.futures
from py2neo import Graph, Node


def process_file(i):
    path = "./neo4jInit/data/spider_data"
    target_path = "./neo4jInit/data/new_data/"
    # 载入path
    with open(os.path.join(path, str(i) + ".json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    # 需要的数据
    dict = {}
    dict["name"] = data["basic_info"]["name"]
    dict["desc"] = data["basic_info"]["desc"]
    dict["category"] = data["basic_info"]["category"][1:-1]
    dict["health_insuranc"] = (
        data["basic_info"]["attributes"][0].split("：")[1].replace(" ", "")
    )
    dict["disease_proportion"] = data["basic_info"]["attributes"][1].split("：")[1]
    dict["susceptible_population"] = (
        data["basic_info"]["attributes"][2].split("：")[1].replace(" ", "")
    )
    dict["mode_of_infection"] = data["basic_info"]["attributes"][3].split("：")[1]
    sym = data["basic_info"]["attributes"][4].split("：")[1]
    words = jieba.lcut(sym)
    dict["complications"] = words
    seg_list = jieba.lcut(
        data["basic_info"]["attributes"][5].split("：")[1], cut_all=False
    )
    seg_list = [x for x in seg_list if x != " "]
    dict["medical_department"] = seg_list
    dict["mode_of_treatment"] = (
        data["basic_info"]["attributes"][6].split("：")[1].split(" ")
    )
    dict["treatment_cycle"] = data["basic_info"]["attributes"][7].split("：")[1]
    dict["cure_rate"] = (
        data["basic_info"]["attributes"][8].split("：")[1].replace(" ", "")
    )
    dict["treatment_cost"] = data["basic_info"]["attributes"][9].split("：")[1]
    dict["recommend"] = data["basic_info"]["attributes"][10]
    dict["cause"] = data["cause_info"]
    dict["prevention"] = data["prevent_info"]
    dict["symptom"] = data["symptom_info"][0]
    dict["concrete_performance"] = data["symptom_info"][1]
    dict["inspect"] = data["inspect_info"]
    dict["diet_and_health_care"] = data["food_info"]["good"]
    dict["avoid_eating_food"] = data["food_info"]["bad"]
    dict["recommend_food"] = data["food_info"]["recommand"]
    dict["commonly_used_drugs"] = data["common_drug"]
    dict["drug_detail"] = data["drug_detail"]
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


if __name__ == "__main__":
    prepare_data()
    # create_diseases()
