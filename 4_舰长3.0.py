import requests
import re
import csv
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# 将数据存放在databilibili3.0中
fp = open("databili3.0.csv", mode="w", encoding="utf8", newline="")
csvwriter = csv.writer(fp)


def captain_page_num(uid, roomid):
    # 访问舰长数据页，获取page数和舰长总数
    url = "https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList?" \
          "roomid="+roomid+"&page=1&ruid="+uid+"&page_size=29"
    resp = requests.get(url)
    # 利用re查询舰长总数，已经舰长页数
    page_data = re.compile(r'{"num":(?P<num>.*?),"page":(?P<page>.*?),"', re.S)
    captain_num = page_data.search(resp.text).group("num")
    page_num = page_data.search(resp.text).group("page")
    print("舰长总数为：%s" % captain_num)
    # print(page_num)
    # 返回得到的页码数
    page_num = int(page_num)
    return page_num


def captain_list(url):
    resp = requests.get(url)
    # 获取resp里面的舰长uid和name数据
    name_data = re.compile(r'"uid":(?P<uid>.*?),".*?,"rank":(?P<rank>.*?),"username":"(?P<name>.*?)",', re.S)
    name_page = name_data.finditer(resp.text)
    resp.close()
    # 将页面获得的数据存入
    for it in name_page:
        # print(it.group("name"))
        dic = it.groupdict()
        csvwriter.writerow(dic.values())
        # fp.close()


def run(uid, roomid):
    uid = str(uid)
    roomid = str(roomid)
    # 输出舰长总数，提取page数
    page_num = captain_page_num(uid, roomid)
    # 利用多进程加速运算
    with ThreadPoolExecutor(50) as t:
        for i in tqdm(range(page_num+1)):
            t.submit(captain_list, f"https://api.live.bilibili.com/"
                                   f"xlive/app-room/v2/guardTab/topList?roomid="
                                   f""+roomid+"&"f"page={i}&ruid="+uid+"&page_size=29")
    print("over!")
# 嘉然 uid：672328094，roomid：22637261
# 贝拉 uid：672353429，roomid：22632424


run(672353429, 22632424)




