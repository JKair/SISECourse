# -*- coding: utf-8 -*-
import urllib2
import re
from MysqlHandle import *

listurl = "http://class.sise.com.cn:7001/sise/module/selectclassview/selectclassallcourse_view.jsp"
courseurl = "http://class.sise.com.cn:7001/sise/common/course_view.jsp?id=%s"
preReg = r".*?\(([A-Za-z0-9]*?)\)"

# 正则匹配
# reg  		string 	正则表达式
# html 		string 	需要匹配的字符串
# return	list 	匹配结果
def reg_match(reg, html):
    return re.compile(reg, re.S).findall(html)


# 获取html
# url 		string	链接
# return 	string	拉取结果
def get_html(url):
    return urllib2.urlopen(url).read().decode('gbk', 'replace').encode('utf-8')


# 读取文件内容，获取课程列表
def read_file():
    file_object = open('selectclassallcourse_view.html')
    try:
        all_the_text = file_object.read()
    finally:
        file_object.close()
    _test = re.compile(
        r"<tr\s*?height='25'><td\s*?class='tablebody'\s*?><span\s*?class='font12'>(.+?)</span></td><td\s*?class='tablebody'\s*?><span\s*?class='font12'><a\s*?href='/sise/common/course_view.jsp\?id=(.+?)'\s*?target='_blank'\s*?title='点击显示课程详细信息'>(.+?)</a></span></td><td\s*?class='tablebody'\s*?><span\s*?class='font12'>(.+?)</span></td><td\s*?class='tablebody'\s*?><span\s*?class='font12'>(.+?)</span></td><td\s*?class='tablebody'\s*?><span\s*?class='font12'>(.+?)</span></td></tr>",
        re.S).findall(all_the_text)

    return _test  # 0是课程代码，1是id，2是课程名，3是教学承担系，4是学分，5是考核方式


# 从html获取课程信息
# html 		string	课程的html
# return	dir		包含所需信息的字典
def get_course_info(html):
    _cid = reg_match(
        r'<td  height="0" class="tableBodyright"><span class="font12">代 &nbsp;&nbsp;&nbsp;码</span> ： </td>.*?<td height="0" class="tableBodyleft"><div align="left">(.+?)</div></td>',
        html)
    _examway = reg_match(
        r'<td  height="0" class="tableBodyright"><span class="font12">考核方式</span> ： </td>.*?<td height="0" class="tableBodyleft"><div align="left">(.+?)</div></td>',
        html)
    _credit = reg_match(
        r'<td  height="0" class="tableBodyright"><span class="font12">学 &nbsp;&nbsp;&nbsp;分</span> ： </td>.*?<td height="0" class="tableBodyleft"><div align="left">(.+?)</div></td>',
        html)
    _faculty = reg_match(
        r'<td  height="0" class="tableBodyright"><span class="font12">教学承担系</span> ： </td>.*?<td height="0" class="tableBodyleft"><div align="left">(.+?)</div></td>',
        html)
    _cname = reg_match(
        r'<td  height="0" class="tableBodyright"><span class="font12">名 &nbsp;&nbsp;&nbsp;称</span> ： </td>.*?<td height="0" class="tableBodyleft"><div align="left">(.+?)</div></td>',
        html)
    _detail = reg_match(
        r'<td width="120"  height="50" class="tableBodyright" valign="top">.*?<span class="font12">简&nbsp;&nbsp;&nbsp;&nbsp;介</span> ： </td>.*?<td height="50" class="tableBodyleft" colspan="2" valign="top">.*?<div align="left">(.+?)</div></td>',
        html)

    return {
        'cid': _cid[0].strip(),
        'examway': 0 if _examway[0].strip() == '考查' else 1,
        'credit': _credit[0].strip(),
        'faculty': _faculty[0].strip(),
        'cname': _cname[0].strip(),
        'detail': _detail[0].strip()
    }


# 从html获取先修情况
# html 		string	课程的html
# cid 		string	当前解析课程的代码
# return	string	先修的分析结果
def get_pre(html,cid):
    _pre = reg_match(
        r'<td  height="0" class="tableBodyright"><span class="font12">先修课程 </span>： </td>.*?<td height="0" class="tableBodyleft"><div align="left">(.+?)</div></td>',
        html)
    token = ""
    strResult = _pre[0].strip()
    preResult = []
    _group = 0
    # 先修判断
    if strResult.find('和') != -1:
    	if strResult.find('或') != -1:
    		strResult = strResult.split('或')
    		for row in strResult:
    			row = row.split('和')
    			for preAnd in row:
    				if preAnd.find('(') == -1:
	    				token = preAnd
	    				continue
    				preAnd = token + preAnd
    				preRow = reg_match(preReg,preAnd)[0]
    				preResult.append((cid,preRow,_group))
    			_group += 1
    	else:
    		strResult = strResult.split('和')
    		for row in strResult:
    			if row.find('(') == -1:
    				token = row
    				continue
    			row = token + row
    			preRow = reg_match(preReg,row)[0]
    			preResult.append((cid,preRow,_group))
    			_group += 1
    	return preResult
    elif strResult.find('或') != -1:
    	strResult = strResult.split('或')
    	for row in strResult:
    		if row.find('(') == -1:
    			token = row
    			continue
    		row = token + row
    		preRow = reg_match(preReg,row)[0]
    		preResult.append((cid,preRow,_group))
    		_group += 1
    	return preResult
    else:
    	return False

if __name__ == '__main__':
    handle = MysqlHandle()
    for row in read_file():
    	courseInfo = get_course_info(get_html(courseurl % row[1]))
        sql = sql="INSERT INTO cs_course(cid,examway,credit,faculty,cname,detail) VALUES('%s','%s','%s','%s','%s','%s')" %(courseInfo['cid'],courseInfo['examway'],courseInfo['credit'],courseInfo['faculty'],courseInfo['cname'],courseInfo['detail'])
        if handle.execute_sql(sql) == False :
			print "error"
        pre = get_pre(get_html(courseurl % row[1]),courseInfo["cid"])
        if pre != False:
        	for row in pre:
        		sql="INSERT INTO cs_pre(aim,pre,_group) VALUES('%s','%s','%s')" %(row[0],row[1],row[2])
        		if handle.execute_sql(sql) == False :
					print "error"