import requests
import re


def search_vol(name):
    name = str(name)
    i, m = 0, 0
    a = []
    # 获取搜索页面的最高播放量数据
    url = "https://search.bilibili.com/all?keyword="+name+"&order=click"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    resp = requests.get(url, headers=header)
    # 获取作品数据，作品名字跟播放量
    main = re.compile(r'</span><a title="(?P<name>.*?)" href=.*?<i class="icon-playtime">'
                      r'</i>(?P<vol>.*?)</span>', re.S)
    # 获取作品aid
    main_aid = re.compile(r'"aid":(?P<aid>.*?),"bvid"', re.S)
    vol = main.finditer(resp.text)
    aid = main_aid.finditer(resp.text)
    # 利用作品aid跟tag比较，是否是我们搜索对象
    for it in aid:
        aid = str(it.group("aid"))
        url = "https://api.bilibili.com/x/web-interface/view/detail/tag?aid="+aid
        resp = requests.get(url)
        tag_page = re.compile(r'"tag_name":"(?P<tag>.*?)","')
        tag_list = tag_page.finditer(resp.text)
        i += 1
        for itt in tag_list:
            if itt.group("tag") == name:
                a.append(i)
    # a列表就是达要求的作品顺序
    for it in vol:
        m += 1
        if m == a[0]:
            # a[0]为最高播放量作品
            print(name, end=" 最高播放量作品：")
            print(it.group("name"), end="  ")
            print(it.group("vol").strip())


search_vol("向晚")
search_vol("贝拉")
search_vol("珈乐")
search_vol("嘉然")
search_vol("乃琳")








