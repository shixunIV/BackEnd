import requests
import os


def spiders():
    base_url = "https://jib.xywy.com/"
    # 爬取全部的10137个疾病
    for i in range(1, 10138):
        url = base_url + "il_sii_" + str(i) + ".htm"
        # 获得页面
        response = requests.get(url).text
        # 解析页面
        response = response.split("\n")
        # body/div/div/div/div
        print(response)
        return


if __name__ == "__main__":
    spiders()
