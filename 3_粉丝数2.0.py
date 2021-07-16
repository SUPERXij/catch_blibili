import requests
import re
from time import strftime, localtime


def up_pic_name(uid, k):
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
    if k == "是":
        path = name + ".png"
        # ./images/me1.png
        with open(path, 'wb') as fp:
            fp.write(resp_pic.content)
    resp_url.close()
    resp_pic.close()
    print(name, end="")


def up_info(uid, k):
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
    up_pic_name(uid, k)
    print("的粉丝数：" + fan_number)
    resp.close()


def sreach_name(name):
    up_name = str(name)
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    search_url = "https://search.bilibili.com/upuser?keyword=" + up_name
    resp_search_url = requests.get(search_url, headers=header)
    up_web = re.compile(r'<div class="up-face"><a href="(?P<uid>.*?)" title="', re.S)
    up_url = up_web.search(resp_search_url.text).group("uid")
    up_uid = "".join(re.findall(r"\d+", up_url))
    resp_search_url.close()
    return up_uid

# up_info(351609538) name = "珈乐Carol"


def run():
    print("输入up主id或uid可以查询粉丝数")
    print("输入1进行id查询，输入2进行uid查询")
    i = int(input("请选择："))
    if i == 1:
        name = input("请输入up主id:")
        k = input("是否生成up头像：(是/否)")
        uid = sreach_name(name)
        up_info(uid, k)
    elif i == 2:
        uid = input("请输入up主uid:")
        k = input("是否输出up头像：(是/否)")
        up_info(uid, k)
    else:
        print("输入错误请重试！")


run()
