import requests
import re
import itertools
import time
from tqdm import tqdm


uid_temp = []
n = 0
level1, level2, level3, level4, level5, level6 = 0, 0, 0, 0, 0, 0

for i in tqdm(range(1, 400)):
    url = f"https://api.live.bilibili.com/xlive/app-room/v2/guardTab/" \
          f"topList?roomid=22632424&page={i}&ruid=672353429&page_size=29"
    resp = requests.get(url)
    uid_data = re.compile(r'"uid":(?P<uid>.*?),"', re.S)
    uid_page = uid_data.finditer(resp.text)
    uid = itertools.chain(uid_temp, uid_page)
    uid_temp = uid
    resp.close()

for it in tqdm(uid):
    # print(it.group("uid"))
    uid_number = str(it.group("uid"))
    url = "https://api.bilibili.com/x/space/acc/info?mid="+uid_number+"&jsonp=jsonp"
    resp = requests.get(url)
    level_data = re.compile(r'"level":(?P<level>.*?),"', re.S)
    level = level_data.search(resp.text).group("level")
    resp.close()
    time.sleep(0.5)
    # print(level)
    n += 1
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

print("1级用户:%d" % level1)
print("2级用户:%d" % level2)
print("3级用户:%d" % level3)
print("4级用户:%d" % level4)
print("5级用户:%d" % level5)
print("6级用户:%d" % level6)
print("统计%d个用户" % n)


