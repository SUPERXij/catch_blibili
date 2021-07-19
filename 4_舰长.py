import requests
import re
import csv
import itertools
from tqdm import tqdm

result1 = []
for i in tqdm(range(0, 400)):
    url = f"https://api.live.bilibili.com/xlive/app-room/v2/guardTab/" \
          f"topList?roomid=22632424&page={i}&ruid=672353429&page_size=29"
    resp = requests.get(url)
    name_data = re.compile(r'"uid":(?P<uid>.*?),".*?"username":"(?P<name>.*?)",', re.S)
    name = name_data.finditer(resp.text)
    result = itertools.chain(result1, name)
    result1 = result
    resp.close()

fp = open("databili.csv", mode="w", encoding="utf8", newline="")
csvwriter = csv.writer(fp)

for it in result:
    # print(it.group("name"))
    dic = it.groupdict()
    csvwriter.writerow(dic.values())

fp.close()
print("over!")
