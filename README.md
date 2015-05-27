华软的课程爬虫
==============


1. 这个爬虫主要是爬取华软的所有选课信息的
1. 因为懒，没去做模拟登陆，爬取课程信息的时候，需要[登录进去](http://class.sise.com.cn:7001/sise/module/selectclassview/selectclassallcourse_view.jsp)，拿一个所有课程信息的html，这样就可以直接爬取所有课程信息了
1. 数据库结构很简单，不知道怎么解释，最主要是pre，处理先修关系
1. 数据库处理在`MysqlHandle`
1. 其他的有注释，自己看