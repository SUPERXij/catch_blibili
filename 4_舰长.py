import requests
import re
import csv
import itertools
from tqdm import tqdm


def captain_list(uid, roomid):
    # 新建一个name_temp的空列表,用于暂时储存每次遍历的name数据
    name_temp = []
    uid = str(uid)
    roomid = str(roomid)
    # 访问舰长数据页，获取page数和舰长总数
    url = "https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList?" \
          "roomid=" + roomid + "&page=1&ruid=" + uid + "&page_size=29"
    resp = requests.get(url)
    page_data = re.compile(r'{"num":(?P<num>.*?),"page":(?P<page>.*?),"', re.S)
    captain_num = page_data.search(resp.text).group("num")
    page_num = page_data.search(resp.text).group("page")
    print("舰长总数为：%s" % captain_num)
    # print(page_num)
    page_num = int(page_num)

    resp.close()
    # range里面的数据看舰长数情况定
    for i in tqdm(range(page_num+1)):
        # 根据uid查询舰长数据
        url = f"https://api.live.bilibili.com/xlive/app-room/" \
              f"v2/guardTab/topList?roomid="+roomid+"&" \
              f"page={i}&ruid="+uid+"&page_size=29"
        resp = requests.get(url)
        # 获取resp里面的舰长uid和name数据
        name_data = re.compile(r'"uid":(?P<uid>.*?),".*?,"rank":(?P<rank>.*?),"username":"(?P<name>.*?)",', re.S)
        name_page = name_data.finditer(resp.text)
        # 将每次遍历的name存储
        name = itertools.chain(name_temp, name_page)
        name_temp = name
        resp.close()

    # 将数据存放在databilibili中
    fp = open("databili.csv", mode="w", encoding="utf8", newline="")
    csvwriter = csv.writer(fp)

    for it in name:
        # print(it.group("name"))
        dic = it.groupdict()
        csvwriter.writerow(dic.values())

    fp.close()
    print("over!")

# 嘉然 uid：672328094，roomid：22637261
# 贝拉 uid：672353429，roomid：22632424


captain_list(672328094, 22637261)
