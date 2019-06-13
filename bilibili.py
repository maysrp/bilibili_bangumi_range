import requests
from requests import Session
from tinydb import TinyDB,Query
from lxml import etree
import time,os


def mdata(rep):
    lix=[]
    html=etree.HTML(rep.text)
    alls=html.xpath("//*[@class='info']")
    j=1
    for i in alls:
        xd=dict(name=i.xpath("a/text()")\
        ,url=i.xpath("a/@href")\
        ,info=i.xpath("div[@class='bangumi-info']/text()")\
        ,play=i.xpath("div[@class='detail']/span[1]/text()")\
        ,mark=i.xpath("div[@class='detail']/span[2]/text()")\
        ,like=i.xpath("div[@class='detail']/span[3]/text()")\
        ,num=j )
        # print("近3日排名",j,"剧名",name,"播放量",play,"订阅数",mark,"喜欢人数",like)
        j+=1
        lix.append(xd)
    return lix

db=TinyDB('bilibili.json')
S=Session()
Q=Query()
urls={3:"https://www.bilibili.com/ranking/bangumi/13/0/3",7:"https://www.bilibili.com/ranking/bangumi/13/0/7",30:"https://www.bilibili.com/ranking/bangumi/13/0/3"}
headers={"Origin": "https://www.bilibili.com/ranking/bangumi/13/0/3","Referer": "https://www.bilibili.com/","User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"}

bangumi=db.table('bangumi')
for i in urls:
    headers['Origin']=urls[i]
    rep=S.get(urls[i],headers=headers)
    ends=mdata(rep)
    xx=time.localtime()
    data=dict(year=xx.tm_year,mon=xx.tm_mon,day=xx.tm_mday,type=i)
    for j in ends:
        for k in j:
            data[k]=j[k]
        if not bangumi.search((Q.day==data['day'])&(Q.mon==data['mon'])&(Q.year==data['year'])&(Q.type==data['type'])&(Q.url==data['url'])):
            bangumi.insert(data)
