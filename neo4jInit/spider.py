import requests
import os
import lxml
from bs4 import BeautifulSoup
import json
import concurrent.futures


class Spider:
    def __init__(self) -> None:
        pass

    def get_html(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        response.encoding = "gbk"  # 设置解码方式为gbk
        html = response.text
        return html

    def basicinfo_spider(self, url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        title = soup.select("title")[0].get_text()
        category = [
            element.get_text() for element in soup.select("div.wrap.mt10.nav-bar a")
        ]
        desc = [
            element.get_text()
            .replace("\r", "")
            .replace("\n", "")
            .replace("\xa0", "")
            .replace("   ", "")
            .replace("\t", "")
            for element in soup.select("div.jib-articl-con.jib-lh-articl p")
        ]
        ps = soup.select("div.mt20.articl-know p")
        infobox = []
        for p in ps:
            info = (
                p.get_text()
                .replace("\r", "")
                .replace("\n", "")
                .replace("\xa0", "")
                .replace("   ", "")
                .replace("\t", "")
            )
            infobox.append(info)
        basic_data = {}
        basic_data["category"] = category
        basic_data["name"] = title.split("的简介")[0]
        basic_data["desc"] = desc
        basic_data["attributes"] = infobox
        return basic_data

    def p_spider(self, url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        ps = soup.select("p")
        data = ""
        for p in ps:
            data += (
                p.get_text()
                .replace("\r", "")
                .replace("\n", "")
                .replace("\xa0", "")
                .replace("   ", "")
                .replace("\t", "")
            )
        return data

    def symptom_spider(self, url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        symptom = [element.get_text() for element in soup.select("a.gre")]
        symptoms = []
        symptoms.append(symptom)
        ps = soup.select("p")
        data = ""
        for p in ps:
            data += (
                p.get_text()
                .replace("\r", "")
                .replace("\n", "")
                .replace("\xa0", "")
                .replace("   ", "")
                .replace("\t", "")
            )
        symptoms.append([data])
        return symptoms

    def inspect_spider(self, url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        inspects = [
            element.get("href") for element in soup.select("li.check-item a.gre")
        ]
        data = []
        for element in inspects:
            html = self.get_html(element)
            soup = BeautifulSoup(html, "html.parser")
            data.append(
                soup.select("div.headings.f12.fYaHei.gray-a.mt10 a")[2].get_text()
            )

        return data

    def treat_spider(self, url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        tag = [element.get_text() for element in soup.select("span.tr.txt-left.fl")]
        trests = [element.get_text() for element in soup.select("span.fl.txt-right")]
        data = {}
        for i in range(len(tag)):
            data[tag[i][:-1]] = trests[i]
        return data

    def food_spider(self, url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        divs = soup.find_all("div", class_="diet-img clearfix mt20")
        food_data = {}
        try:
            food_data["good"] = [
                element.get_text() for element in divs[0].find_all("p")
            ]
            food_data["bad"] = [element.get_text() for element in divs[1].find_all("p")]
            food_data["recommand"] = [
                element.get_text() for element in divs[2].find_all("p")
            ]
        except:
            food_data["good"] = []
            food_data["bad"] = []
            food_data["recommand"] = []
        return food_data

    def drug_spider(self, url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        drugs = [
            i.get_text().replace("\n", "").replace("\t", "").replace(" ", "")
            for i in soup.select("div.fl.drug-pic-rec.mr30 p a")
        ]
        return drugs

    def process_page(self, page):
        basic_url = "http://jib.xywy.com/il_sii/gaishu/%s.htm" % page  # 疾病描述
        cause_url = "http://jib.xywy.com/il_sii/cause/%s.htm" % page  # 疾病起因
        prevent_url = "http://jib.xywy.com/il_sii/prevent/%s.htm" % page  # 疾病预防
        symptom_url = "http://jib.xywy.com/il_sii/symptom/%s.htm" % page  # 疾病症状
        inspect_url = "http://jib.xywy.com/il_sii/inspect/%s.htm" % page  # 疾病检查
        treat_url = "http://jib.xywy.com/il_sii/treat/%s.htm" % page  # 疾病治疗
        food_url = "http://jib.xywy.com/il_sii/food/%s.htm" % page  # 饮食治疗
        drug_url = "http://jib.xywy.com/il_sii/drug/%s.htm" % page  # 药物
        data = {}
        data["url"] = basic_url
        data["basic_info"] = self.basicinfo_spider(basic_url)
        data["cause_info"] = self.p_spider(cause_url)
        data["prevent_info"] = self.p_spider(prevent_url)
        data["symptom_info"] = self.symptom_spider(symptom_url)
        data["inspect_info"] = self.inspect_spider(inspect_url)
        data["treat_info"] = self.treat_spider(treat_url)
        data["food_info"] = self.food_spider(food_url)
        data["drug_info"] = self.drug_spider(drug_url)
        print(page, basic_url)
        # 保存为json
        with open("neo4jInit/data/%s.json" % page, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def spiders(self):
        base_url = "https://jib.xywy.com/"
        # 爬取全部的10137个疾病,多线程就是吊
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.process_page, range(1, 10138))


if __name__ == "__main__":
    spider = Spider()
    spider.spiders()
