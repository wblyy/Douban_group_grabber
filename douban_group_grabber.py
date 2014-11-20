 # encoding: UTF-8
#first_group='http://www.douban.com/group/'+group_id+'/discussion?start=0'
#			first_group_view=urllib2.urlopen(first_group).read()
#			page_view=re.findall(('<a href="http://www.douban.com/group/'+group_id+'/discussion?start=(.*?)" >').decode('utf-8').encode('utf-8'), first_group_view, re.DOTALL)
			#pagenumber=page_view
#			print 'page_view=',page_view
import ConfigParser
import re
import urllib2
import urllib
import time
from mydbV2 import MydbV2

dbV2 = MydbV2()
conf = ConfigParser.ConfigParser()
conf.read("douban_group.conf")
url_index_start=int(conf.get("douban_group", "url_index_start"))
group_id_start=conf.get("douban_group", "group_id_start")
topic_id_start=conf.get("douban_group", "topic_id_start")
group_index_start=int(conf.get("douban_group", "group_index_start"))
topic_index_start=int(conf.get("douban_group", "topic_index_start"))

#douban_group.conf

for  url_index in xrange(url_index_start,6520,20):
	conf.set("douban_group", "url_index_start", url_index)
	conf.write(open("douban_group.conf", "w"))  

	try:
		#time.sleep(2)
		page_url='http://www.douban.com/group/explore?start='+str(url_index)+'&tag=%E9%9F%B3%E4%B9%90'
		print page_url
		msg=urllib2.urlopen(page_url).read()
		group=re.findall('<a class="nbg" href="http://www.douban.com/group/(.*?)/" onclick="'.decode('utf-8').encode('utf-8'), msg, re.DOTALL)
		print group
		for group_id_index in xrange(group.index(group_id_start),len(group)):
			conf.set("douban_group", "group_id_start", group_id_index)
			conf.write(open("douban_group.conf", "w"))  

			group_id=group[group_id_index]
			print group_id.decode('utf-8').encode('utf-8')
			group_index=group_index_start
			is_next_page=True
			while is_next_page:
				is_next_page=False
				#time.sleep(10)
				group_url='http://www.douban.com/group/'+group_id+'/discussion?start='+str(group_index)
				print group_url



				group_view=urllib2.urlopen(group_url).read()
				topic=re.findall('http://www.douban.com/group/topic/(.*?)/" title="'.decode('utf-8').encode('utf-8'), group_view, re.DOTALL)
				for topic_id_index in xrange(0,len(topic)):
					conf.set("douban_group", "topic_id_start", topic_id_index)
					conf.write(open("douban_group.conf", "w"))  

					topic_id=topic[topic_id_index]
					print 'group_id:',group_id,'group_index:',group_index,'topic_id:',topic_id
					is_next_comment=True
					topic_index=topic_index_start
					while is_next_comment:
						is_next_comment=False
						topic_url='http://www.douban.com/group/topic/'+topic_id+'/?start='+str(topic_index)
						#http://www.douban.com/group/topic/1994213/?start=100
						topic_view=urllib2.urlopen(topic_url).read()
						comment=re.findall('<p class="">(.*?)</p>'.decode('utf-8').encode('utf-8'), topic_view, re.DOTALL)
						comment_time=re.findall('<span class="pubtime">(.*?)</span>'.decode('utf-8').encode('utf-8'), topic_view, re.DOTALL)
									
						for index in range (0,len(comment)):
							#print comment[index].decode('utf-8'),comment_time[index]
							dbV2.insert_douban_data(comment[index].decode('utf-8'),comment_time[index],topic_id,group_id)

						if 'http://www.douban.com/group/people/' in topic_view:
							is_next_comment=True
							topic_index=topic_index+100
							conf.set("douban_group", "topic_index_start", topic_index)
							conf.write(open("douban_group.conf", "w"))  
							
				if len(topic):#抓到的topic数量不为零则翻页
					is_next_page=True
					group_index=group_index+25
					conf.set("douban_group", "group_index_start", group_index)
					conf.write(open("douban_group.conf", "w"))  
					
			#http://www.douban.com/group/Eason/discussion?start=0

	except Exception, e:
		print e
		#time.sleep(5)

#http://www.douban.com/group/explore?start=20&tag=%E9%9F%B3%E4%B9%90