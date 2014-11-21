#-*-coding:utf-8-*-
import requests
import random
proxy_dict=['http://113.11.198.163:2223/',
			#'http://113.11.198.164:2223/',#
			#'http://113.11.198.165:2223/',#
			#'http://113.11.198.166:2223/',#
			'http://113.11.198.167:2223/',
			'http://113.11.198.168:2223/',
			'http://113.11.198.169:2223/',
			]


r = requests.get("http://www.douban.com", 
                 proxies={"http": random.choice(proxy_dict)})
print(r.text)

r = requests.get("http://www.baidu.com", 
                 proxies={"http": random.choice(proxy_dict)})
print(r.text)

r = requests.get("http://www.sina.com", 
                 proxies={"http": random.choice(proxy_dict)})
print(r.text)