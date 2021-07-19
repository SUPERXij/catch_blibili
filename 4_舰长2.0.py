import requests
import re
import itertools
from tqdm import tqdm


result1 = []
level1, level2, level3, level4, level5, level6 = 0, 0, 0, 0, 0, 0

for i in tqdm(range(1, 5)):
    url = f"https://api.live.bilibili.com/xlive/app-room/v2/guardTab/" \
          f"topList?roomid=22632424&page={i}&ruid=672353429&page_size=29"
    resp = requests.get(url)
    uid_data = re.compile(r'"uid":(?P<uid>.*?),"', re.S)
    uid = uid_data.finditer(resp.text)
    result = itertools.chain(result1, uid)
    result1 = result
    resp.close()

for it in result:
    # print(it.group("uid"))
    uid_number = str(it.group("uid"))
    url = "https://api.bilibili.com/x/space/acc/info?mid="+uid_number+"&jsonp=jsonp"
    resp = requests.get(url)
    level_data = re.compile(r'"level":(?P<level>.*?),"', re.S)
    level = level_data.search(resp.text).group("level")
    resp.close()
    # print(level)

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


