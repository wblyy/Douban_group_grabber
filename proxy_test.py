#-*-coding:utf-8-*-
import requests
import random
import re

proxy_dict=['http://113.11.198.163:2223/',
			#'http://113.11.198.164:2223/',#
			#'http://113.11.198.165:2223/',#
			#'http://113.11.198.166:2223/',#
			'http://113.11.198.167:2223/',
			'http://113.11.198.168:2223/',
			'http://113.11.198.169:2223/',
			]



r = requests.get("http://www.douban.com/group/topic/67825487/?start=0", 
                 proxies={"http": random.choice(proxy_dict)}).text

comment=re.findall('<p class="">(.*?)</p>'.decode('utf-8').encode('utf-8'), r, re.DOTALL)

print comment
