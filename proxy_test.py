#-*-coding:utf-8-*-
import requests
proxy_dict=['http://113.11.198.163:2223/',
			'http://113.11.198.164:2223/',
			'http://113.11.198.165:2223/',
			'http://113.11.198.166:2223/',
			'http://113.11.198.167:2223/',
			'http://113.11.198.168:2223/',
			'http://113.11.198.169:2223/',
			]


s = requests.Session()
s.proxies = {"http": "http://61.233.25.166:80"}

r = s.get("http://www.douban.com")
print(r.text)

s.proxies = {"http": "http://61.233.25.163:80"}

r = s.get("http://www.douban.com")
print(r.text)
