# -*- coding: utf-8 -*-
from GetHtml import *
from MysqlHandle import *
import re


getHtml = GetHtml()

#这个正则用来获取所有的信息，主要是取到课程代码和链接 结果示例
#[('\xd1\xa7\xc9\xfa\xb4\xa6', '\xd1\xa1\xd0\xde', 'GE0083', '1.0', '2721.html', '\xc5\xf3\xb1\xb2\xd0\xc4\xc0\xed\xb8\xa8\xb5\xbc\xc0\xed\xc2\xdb\xbb\xf9\xb4\xa1')]
messageRegExp = r"<tr height='25' bgColor='#ffffff'><td ><div align='center'><span class='font12'>(.*?)</span></div></td><td ><div align='center'><span class='font12'>(.*?)</span></div></td><td ><div align='center'><span class='font12'>(.*?)</span></div></td><td ><div align='center'><span class='font12'>(.*?)</span></div></td><td ><div align='center'><span class='font12'><a href='(.*?)'>(.*?)</a></span></div></td></tr>"

#这个正则用来获取课程的时间信息的，结果示例
#['&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '<font>ABG</font>(\xe6\x9d\x8e\xe9\xb8\xa5 1 2 3 4 5 6 7 8\xe5\x91\xa8[A203])']
courseTimeRegExp = r"<td width='10%' align='left' valign='top' class='font12'>(.*?)</td>"

#这个正则用来分析课程信息的
#[('AVK', '\xe7\xbd\x97\xe8\xbe\xbe', '11 12 13 14 15', 'D201')]
courseDetailRegExp = r"<font>(.*?)</font>\((.*?) (.*?)周\[(.*?)\]\)"

#此方法用来获取所有要插入数据库的数据
def get_all():
	thisTermData = []
	allCourseHtml =  getHtml.get_html("http://class.sise.com.cn:7001/sise/coursetemp/courseInfo.html")
	courseMessage = analyze_course_message (messageRegExp,allCourseHtml)
	print (len(courseMessage))
	for fetchBegin in courseMessage:
		courseTime = getHtml.get_html_suffix('/sise/coursetemp/'+fetchBegin[4])
		courseTime = courseTime.decode('gbk').encode('utf-8')
		courseTime = analyze_course_message (courseTimeRegExp,courseTime)
		thisTermData.append(analyze_course_time(courseTime,fetchBegin[2]))
	mysql_data(thisTermData)
	return

#正则表达式分析
#reg    		string	正则表达式
#courseHtml 	string	需要分析的数据源
#return			list	分析结果
def analyze_course_message(reg,courseHtml):
	return re.compile(reg).findall(courseHtml)

#课程时间分析
#courseTime 	string	课程时间的html
#courseCode		string	课程代码
#return 		list	本课程的所有上课时间信息
def analyze_course_time(courseTime,courseCode):
	analyzerResult = []
	for i in range(len(courseTime)):
		if courseTime[i] != '&nbsp;':
			result = analyze_course_message(courseDetailRegExp,courseTime[i])
			for j in range(len(result)):
				classTime = (i/7+1) + (i%7+1)*10 #自定义格式，十位数表示星期，个位数表示第几节课
				data = (courseCode,classTime,result[j][1],result[j][3],result[j][2],result[j][0])
				analyzerResult.append(data)

	return analyzerResult

#把数据插入数据库
#data list 数据
#return 
def mysql_data(data):
	handle = MysqlHandle()
	for mysqlData in data:
		for courseData in mysqlData:
			sql="INSERT INTO cs_cnow(cid,ctime,teacher,classroom,week,class) VALUES('%s','%s','%s','%s','%s','%s')" %(courseData[0],courseData[1],courseData[2],courseData[3],courseData[4],courseData[5])
			if handle.execute_sql(sql) == False :
				print "error"
				return

	handle.close_sql()


if __name__ == '__main__':
	get_all()