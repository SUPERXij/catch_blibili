import requests
import re
import datetime
import time


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


def updata_query(uid):
    url_up_page = "https://api.bilibili.com/x/space/arc/search?mid=" + uid \
                  + "&pn=1&index=1&jsonp=jsonp"
    resp_url_up_page = requests.get(url_up_page)
    new_bv_data = re.compile(r'"bvid":"(?P<bv>.*?)",', re.S)
    new_bv = new_bv_data.search(resp_url_up_page.text).group("bv")
    bv = str(new_bv)
    url_new = "https://www.bilibili.com/video/" + bv
    resp_url_new = requests.get(url_new)
    sub_date = re.compile(r'"uploadDate" content="(?P<time>.*?)">', re.S)
    sub_time = sub_date.search(resp_url_new.text).group("time")
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time_stamp(sub_time, now_time)


def time_stamp(time1, time2):
    time_array1 = time.strptime(time1, "%Y-%m-%d %H:%M:%S")
    time_array2 = time.strptime(time2, "%Y-%m-%d %H:%M:%S")
    timestamp1 = int(time.mktime(time_array1))
    timestamp2 = int(time.mktime(time_array2))
    time_minus(timestamp1, timestamp2)


def time_minus(timestamp1, timestamp2):
    if timestamp1 >= timestamp2:
        seconds = timestamp1 - timestamp2
    else:
        seconds = timestamp2 - timestamp1
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    print("距上次更新已经有：%d天%d小时%d分%02d秒，生产队的驴都不敢这么歇" % (d, h, m, s))


def run():
    print("输入up主id或uid查询up主多久没更新了")
    print("输入1进行id查询，输入2进行uid查询")
    i = int(input("请选择："))
    if i == 1:
        name = input("请输入up主id:")
        uid = sreach_name(name)
        updata_query(uid)
    elif i == 2:
        uid = input("请输入up主uid:")
        updata_query(uid)
    else:
        print("输入错误请重试！")


# 无耻的Frank 珈乐Carol
run()











