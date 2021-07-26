import csv
import requests
import time
import re
from tqdm import tqdm
from collections import Counter


with open('databili3.0.csv', 'r', encoding="utf8") as csvfile:
    reader = csv.reader(csvfile)
    rows = [row for row in reader]
    # print(rows)


def get_level(uid):
    uid_number = uid
    url = "https://api.bilibili.com/x/space/acc/info?mid="+uid_number+"&jsonp=jsonp"
    resp = requests.get(url)
    level_data = re.compile(r'"level":(?P<level>.*?),"', re.S)
    level = level_data.search(resp.text).group("level")
    resp.close()
    # 设置时间限制防止被墙
    time.sleep(0.5)
    # print(level)
    # 将输出的舰长等级统计
    level_number = int(level)
    level_list.append(level_number)
    # 由于舰长名单有重复，所以我们需要人工减


for i in tqdm(rows):
    uid = i[0]
    level_list = []
    get_level(uid)

Counter(level_list)





