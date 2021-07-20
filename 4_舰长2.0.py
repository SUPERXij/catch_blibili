import requests
import re
import itertools
import time
from tqdm import tqdm


def captain_level(uid, roomid):
    uid_temp = []
    level1, level2, level3, level4, level5, level6 = 0, 0, 0, 0, 0, 0
    uid = str(uid)
    roomid = str(roomid)
    # 访问舰长数据页，获取page和舰长数
    url = "https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList?" \
          "roomid="+roomid+"&page=1&ruid="+uid+"&page_size=29"
    resp = requests.get(url)
    page_data = re.compile(r'{"num":(?P<num>.*?),"page":(?P<page>.*?),"', re.S)
    captain_num = page_data.search(resp.text).group("num")
    page_num = page_data.search(resp.text).group("page")
    print("舰长总数为：%s" % captain_num)
    page_num = int(page_num)
    # 遍历获得舰长uid
    for i in tqdm(range(1, page_num+1)):
        url = f"https://api.live.bilibili.com/xlive/app-room/v2/guardTab/" \
              f"topList?roomid="+roomid+"&"f"page={i}&ruid="+uid+"&page_size=29"
        resp = requests.get(url)

        uid_data = re.compile(r'"uid":(?P<uid>.*?),"', re.S)
        uid_page = uid_data.finditer(resp.text)
        uid_all = itertools.chain(uid_temp, uid_page)
        uid_temp = uid_all
        resp.close()
    # 对每个uid访问个人主页获取等级
    for it in tqdm(uid_all):
        # print(it.group("uid"))
        uid_number = str(it.group("uid"))
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
        if level_number == 1:
            level1 += 1
        elif level_number == 2:
            level2 += 1
        elif level_number == 3:
            level3 += 1
        elif level_number == 4:
            level4 += 1
        elif level_number == 5:
            level5 += 1
        else:
            level6 += 1
    # 由于舰长名单有重复，所以我们需要人工减
    print("1级用户:%d" % level1)
    print("2级用户:%d" % level2)
    print("3级用户:%d" % level3)
    print("4级用户:%d" % level4)
    print("5级用户:%d" % (level5-(page_num-1)*2))
    print("6级用户:%d" % (level6-(page_num-1)))


# 嘉然 uid：672328094，roomid：22637261
captain_level(672328094, 22637261)
