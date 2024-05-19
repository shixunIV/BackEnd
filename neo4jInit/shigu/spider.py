import requests
import os
import lxml
from bs4 import BeautifulSoup
import json
import concurrent.futures


class Spider:
    def __init__(self) -> None:
        self.data_path = "neo4jInit/data/railway.json"

    def get_html(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        response = requests.get(url, headers=headers)
        # response.encoding = "gbk"  # 设置解码方式为gbk
        html = response.text
        return html

    def spiders_all(self):
        data = []
        url = "https://zh.wikipedia.org/wiki/%E9%90%B5%E8%B7%AF%E4%BA%8B%E6%95%85%E5%88%97%E8%A1%A8"
        html = self.get_html(url)
        soup = BeautifulSoup(html, "lxml")
        ul_tags = soup.find_all("ul")
        for ul in ul_tags:
            li_tags = ul.find_all("li")
            for li in li_tags:
                data.append(li.text)
        print(data)
        # 把data存入csv文件
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    def spiders_china(self):
        data = []
        url = "https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E9%93%81%E8%B7%AF%E4%BA%8B%E6%95%85%E5%88%97%E8%A1%A8"
        html = self.get_html(url)
        soup = BeautifulSoup(html, "lxml")
        tr_tags = soup.find_all("tr")
        for tr in tr_tags:
            js = {}
            tag = [
                "日期",
                "路线",
                "地点",
                "车次",
                "事故类型",
                "原因",
                "死亡人数",
                "受伤人数",
                "备注",
            ]
            i = 0
            for td in tr.find_all("td"):
                js[tag[i]] = td.text.replace("\n", "")
                i += 1
            data.append(js)
        print(data)
        # 把data存入csv文件
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)


if __name__ == "__main__":
    spider = Spider()
    # spider.spiders()
    spider.spiders_china()
