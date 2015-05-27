/*
Navicat MySQL Data Transfer

Source Server         : ca.sise.com.cn
Source Server Version : 50529
Source Host           : ca.sise.com.cn:3306
Source Database       : course_selection

Target Server Type    : MYSQL
Target Server Version : 50529
File Encoding         : 65001

Date: 2015-05-27 20:38:08
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for cs_cnow
-- ----------------------------
DROP TABLE IF EXISTS `cs_cnow`;
CREATE TABLE `cs_cnow` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '索引ID',
  `cid` char(6) DEFAULT NULL COMMENT '课程编码',
  `ctime` tinyint(4) DEFAULT NULL COMMENT '上课时间：（int）星期*10+第几节，例如 12（星期1第2节）',
  `teacher` varchar(10) DEFAULT NULL COMMENT '老师名字',
  `classroom` varchar(20) DEFAULT NULL COMMENT '教室',
  `week` varchar(50) DEFAULT NULL COMMENT '周数（字符串）',
  `class` varchar(15) DEFAULT NULL COMMENT '教学班',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35171 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for cs_course
-- ----------------------------
DROP TABLE IF EXISTS `cs_course`;
CREATE TABLE `cs_course` (
  `cid` char(6) NOT NULL COMMENT '课程代码',
  `examway` tinyint(4) DEFAULT NULL COMMENT '考试方式，0：考查 1:考试',
  `credit` float(4,1) DEFAULT NULL COMMENT '学分',
  `faculty` varchar(20) DEFAULT NULL COMMENT '教学系',
  `cname` varchar(50) DEFAULT NULL COMMENT '课程名字',
  `detail` varchar(1000) DEFAULT NULL COMMENT '简介',
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for cs_pre
-- ----------------------------
DROP TABLE IF EXISTS `cs_pre`;
CREATE TABLE `cs_pre` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `aim` char(6) DEFAULT NULL COMMENT '目标课程代码',
  `pre` char(20) DEFAULT NULL COMMENT '先修课程代码',
  `_group` tinyint(4) DEFAULT NULL COMMENT '先修分组，欲选修目标课程，必符合其中一个分组',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15603 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for cs_sinformation
-- ----------------------------
DROP TABLE IF EXISTS `cs_sinformation`;
CREATE TABLE `cs_sinformation` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增索引',
  `sid` int(11) DEFAULT NULL COMMENT '学生学号',
  `sname` varchar(10) DEFAULT NULL COMMENT '学生名字',
  `sgrade` smallint(6) DEFAULT NULL COMMENT '年级（年份，4数字）',
  `smajor` varchar(100) DEFAULT NULL COMMENT '所在教学系',
  `expected` float(4,1) DEFAULT NULL COMMENT '预期获得学分',
  `required` float(4,1) DEFAULT NULL COMMENT '必修课的总学分',
  `cchoice` float(4,1) DEFAULT NULL COMMENT '已选修学分',
  `choiced` text COMMENT '已修课程',
  `reading` text COMMENT '在读课程',
  `next` text COMMENT '预修课程',
  `nextCourses` text COMMENT '下学期的课',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1927 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for cs_syllabus
-- ----------------------------
DROP TABLE IF EXISTS `cs_syllabus`;
CREATE TABLE `cs_syllabus` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `sid` int(11) NOT NULL COMMENT '学号',
  `courseID` varchar(255) DEFAULT NULL COMMENT '课程号',
  `divId` varchar(255) DEFAULT NULL COMMENT '放这门课的DIV的ID',
  `checkboxId` varchar(255) DEFAULT NULL COMMENT '复选框的ID',
  `place` varchar(255) DEFAULT NULL COMMENT '位置',
  `content` varchar(255) DEFAULT NULL COMMENT '内容',
  `week` varchar(255) DEFAULT NULL COMMENT '周数',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43605 DEFAULT CHARSET=utf8;
