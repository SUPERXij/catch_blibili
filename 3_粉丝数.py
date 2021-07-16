import requests
import re
from time import strftime, localtime


def up_pic_name(uid):
    uid = str(uid)
    url = "https://api.bilibili.com/x/space/acc/info?mid="+uid+"&jsonp=jsonp"
    resp_url = requests.get(url)
    # 获取up主名字信息
    name_data = re.compile(r'"name":"(?P<name>.*?)",', re.S)
    # 获取up主头像信息
    pic_data = re.compile(r'"face":"(?P<pic>.*?)",', re.S)
    pic_url = pic_data.search(resp_url.text).group("pic")
    resp_pic = requests.get(pic_url)
    name = name_data.search(resp_url.text).group("name")
    path = name + ".png"
    # ./images/me1.png
    with open(path, 'wb') as fp:
        fp.write(resp_pic.content)
    resp_url.close()
    resp_pic.close()
    print(name, end="")


def up_info(uid):
    uid = str(uid)
    # 获取uid
    url = "https://api.bilibili.com/x/relation/stat?vmid=" + uid + "&jsonp=jsonp"
    # 通过url爬取到数据
    resp = requests.get(url)
    # re查找粉丝数
    data = re.compile(r'"follower":(?P<num>.*?)}', re.S)
    fan_number = data.search(resp.text).group("num")

    print(strftime("%Y", localtime()) + "年" + strftime("%m", localtime()) + "月" +
          strftime("%d", localtime()) + "日"" ", end="")
    up_pic_name(uid)
    print("的粉丝数：" + fan_number)
    resp.close()


up_info(351609538)
