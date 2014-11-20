 # encoding: UTF-8
#first_group='http://www.douban.com/group/'+group_id+'/discussion?start=0'
#			first_group_view=urllib2.urlopen(first_group).read()
#			page_view=re.findall(('<a href="http://www.douban.com/group/'+group_id+'/discussion?start=(.*?)" >').decode('utf-8').encode('utf-8'), first_group_view, re.DOTALL)
			#pagenumber=page_view
#			print 'page_view=',page_view

import re
import urllib2
import urllib
import time
from mydbV2 import MydbV2

dbV2 = MydbV2()

for  url_index in xrange(0,6520,20):
	try:
		#time.sleep(2)
		page_url='http://www.douban.com/group/explore?start='+str(url_index)+'&tag=%E9%9F%B3%E4%B9%90'
		print page_url
		msg=urllib2.urlopen(page_url).read()
		group=re.findall('<a class="nbg" href="http://www.douban.com/group/(.*?)" onclick="'.decode('utf-8').encode('utf-8'), msg, re.DOTALL)
		for group_id in group:
			print group_id.decode('utf-8').encode('utf-8')
			group_index=0
			is_next_page=True
			while is_next_page:
				is_next_page=False
				#time.sleep(10)
				group_url='http://www.douban.com/group/'+group_id+'/discussion?start='+str(group_index)
				group_view=urllib2.urlopen(group_url).read()
				topic=re.findall('http://www.douban.com/group/topic/(.*?)/" title="'.decode('utf-8').encode('utf-8'), group_view, re.DOTALL)
				for topic_id in topic:
					#print 'group_id:',group_id,'group_index:',group_index,'topic_id:',topic_id
					is_next_comment=True
					topic_index=0
					while is_next_comment:
						is_next_comment=False
						topic_url='http://www.douban.com/group/topic/'+topic_id+'/?start='+str(topic_index)
						#http://www.douban.com/group/topic/1994213/?start=100
						topic_view=urllib2.urlopen(topic_url).read()
						comment=re.findall('<p class="">(.*?)</p>'.decode('utf-8').encode('utf-8'), topic_view, re.DOTALL)
						comment_time=re.findall('<span class="pubtime">(.*?)</span>'.decode('utf-8').encode('utf-8'), topic_view, re.DOTALL)
						#print 'time-lenth',len(comment_time),'commenti-lenth',len(comment)
						#print comment_time[0]
						#<span class="pubtime"> *** </span>
						#<p class=""> *** </p>
						
						for index in range (0,len(comment)):
							#print comment[index].decode('utf-8'),comment_time[index]
							dbV2.insert_douban_data(comment[index].decode('utf-8'),comment_time[index],topic_id,group_id)
							#print 'group_id:',group_id,'group_index:',group_index,'topic_id:',topic_id,'topic_index',topic_index,comment[index].decode('utf-8'),comment_time[index]
							#http://www.douban.com/group/people/
						if 'http://www.douban.com/group/people/' in topic_view:
							is_next_comment=True
							topic_index=topic_index+100
							
				if len(topic):#抓到的topic数量不为零则翻页
					is_next_page=True
					group_index=group_index+25
					
			#http://www.douban.com/group/Eason/discussion?start=0

	except Exception, e:
		print e
		#time.sleep(5)

#http://www.douban.com/group/explore?start=20&tag=%E9%9F%B3%E4%B9%90