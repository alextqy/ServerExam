-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        8.0.32 - MySQL Community Server - GPL
-- 服务器操作系统:                      Win64
-- HeidiSQL 版本:                  12.0.0.6536
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- 导出 server-exam 的数据库结构
CREATE DATABASE IF NOT EXISTS `server-exam` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `server-exam`;

-- 导出  表 server-exam.class 结构
CREATE TABLE IF NOT EXISTS `class` (
  `ID` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '创建时间',
  `ClassName` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '班级名称',
  `ClassCode` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '班级代码',
  `Description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '班级描述',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='班级';

-- 正在导出表  server-exam.class 的数据：~3 rows (大约)

-- 导出  表 server-exam.examinee 结构
CREATE TABLE IF NOT EXISTS `examinee` (
  `ID` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '创建时间',
  `ExamineeNo` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '考生编号',
  `Name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '考生姓名',
  `ClassID` int(10) unsigned zerofill DEFAULT NULL COMMENT '班级ID',
  `Contact` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '联系方式',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考生';

-- 正在导出表  server-exam.examinee 的数据：~6 rows (大约)

-- 导出  表 server-exam.examineetoken 结构
CREATE TABLE IF NOT EXISTS `examineetoken` (
  `ID` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT COMMENT '考生token',
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '创建时间',
  `Token` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '考生token',
  `ExamID` int(10) unsigned zerofill DEFAULT NULL COMMENT '报名ID',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考生token';

-- 正在导出表  server-exam.examineetoken 的数据：~0 rows (大约)

-- 导出  表 server-exam.examinfo 结构
CREATE TABLE IF NOT EXISTS `examinfo` (
  `ID` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '创建时间',
  `SubjectName` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '科目名称',
  `ExamNo` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '准考证号',
  `TotalScore` decimal(10,2) unsigned zerofill DEFAULT NULL COMMENT '总分',
  `PassLine` decimal(10,2) unsigned zerofill DEFAULT NULL COMMENT '及格线',
  `ActualScore` decimal(10,2) unsigned zerofill DEFAULT NULL COMMENT '实际得分',
  `ExamDuration` int(10) unsigned zerofill DEFAULT NULL COMMENT '额定考试时长',
  `StartTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '实际考试开始时间',
  `EndTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '额定考试结束时间',
  `ActualDuration` int(10) unsigned zerofill DEFAULT NULL COMMENT '实际考试时长',
  `Pass` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '是否通过 1否 2是',
  `UpdateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '更新时间',
  `ExamineeID` int(10) unsigned zerofill DEFAULT NULL COMMENT '考生ID',
  `ExamState` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '考试状态 1没有答题卡 2待考(已经生成答题卡) 3已考试 4作废',
  `ExamType` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '考试类型 1正式考试 2练习',
  `StartState` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '开始状态 1未开始 2已开始',
  `SuspendedState` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '暂停状态 1正常 2暂停',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='报名';

-- 正在导出表  server-exam.examinfo 的数据：~3 rows (大约)

-- 导出  表 server-exam.examinfohistory 结构
CREATE TABLE IF NOT EXISTS `examinfohistory` (
  `ID` int(10) unsigned zerofill NOT NULL,
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '创建时间',
  `SubjectName` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '科目名称',
  `ExamNo` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '准考证号',
  `TotalScore` decimal(10,2) unsigned zerofill DEFAULT NULL COMMENT '总分',
  `PassLine` decimal(10,2) unsigned zerofill DEFAULT NULL COMMENT '及格线',
  `ActualScore` decimal(10,2) unsigned zerofill DEFAULT NULL COMMENT '实际得分',
  `ExamDuration` int(10) unsigned zerofill DEFAULT NULL COMMENT '额定考试时长',
  `StartTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '实际考试开始时间',
  `EndTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '额定考试结束时间',
  `ActualDuration` int(10) unsigned zerofill DEFAULT NULL COMMENT '实际考试时长',
  `Pass` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '是否通过 1否 2是',
  `UpdateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '更新时间',
  `ExamineeID` int(10) unsigned zerofill DEFAULT NULL COMMENT '考生ID',
  `ExamState` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '考试状态 1没有答题卡 2待考(已经生成答题卡) 3已考试 4作废',
  `ExamType` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '考试类型 1正式考试 2练习',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='历史报名';

-- 正在导出表  server-exam.examinfohistory 的数据：~0 rows (大约)

-- 导出  表 server-exam.examlog 结构
CREATE TABLE IF NOT EXISTS `examlog` (
  `ID` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '创建时间',
  `Type` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '日志类型 1操作 2登录',
  `ExamNo` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '准考证号',
  `Description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '描述信息',
  `IP` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'IP地址',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考试日志';

-- 正在导出表  server-exam.examlog 的数据：~0 rows (大约)

-- 导出  表 server-exam.headline 结构
CREATE TABLE IF NOT EXISTS `headline` (
  `ID` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '创建时间',
  `Content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '内容',
  `ContentCode` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '内容代码',
  `UpdateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='大标题';

-- 正在导出表  server-exam.headline 的数据：~9 rows (大约)

-- 导出  表 server-exam.knowledge 结构
CREATE TABLE IF NOT EXISTS `knowledge` (
  `ID` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '创建时间',
  `KnowledgeName` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '知识点名称',
  `KnowledgeCode` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '知识点代码',
  `SubjectID` int(10) unsigned zerofill DEFAULT NULL COMMENT '科目ID',
  `KnowledgeState` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '知识点状态 1正常 2禁用',
  `UpdateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='知识点';

-- 正在导出表  server-exam.knowledge 的数据：~2 rows (大约)

-- 导出  表 server-exam.manager 结构
CREATE TABLE IF NOT EXISTS `manager` (
  `ID` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '创建时间',
  `Account` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '账号',
  `Password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '密码',
  `Name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '名称',
  `State` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '状态 1正常 2禁用',
  `Permission` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '权限 9 ~ 1 从高到低',
  `UpdateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '更新时间',
  `Token` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'token',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='管理员';

-- 正在导出表  server-exam.manager 的数据：~1 rows (大约)
INSERT IGNORE INTO `manager` (`ID`, `CreateTime`, `Account`, `Password`, `Name`, `State`, `Permission`, `UpdateTime`, `Token`) VALUES
	(0000000001, 1651887805, 'root', '5f1d7a84db00d2fce00b31a7fc73224f', 'admin', 1, 9, 1675154211, '');

-- 导出  表 server-exam.paper 结构
CREATE TABLE IF NOT EXISTS `paper` (
  `ID` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '创建时间',
  `PaperName` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '试卷名称',
  `PaperCode` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '试卷代码',
  `SubjectID` int(10) unsigned zerofill DEFAULT NULL COMMENT '科目ID',
  `TotalScore` decimal(10,2) unsigned zerofill DEFAULT NULL COMMENT '总分',
  `PassLine` decimal(10,2) unsigned zerofill DEFAULT NULL COMMENT '及格线',
  `ExamDuration` int(10) unsigned zerofill DEFAULT NULL COMMENT '考试时长',
  `PaperState` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '试卷状态 1正常 2禁用',
  `UpdateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='试卷';

-- 正在导出表  server-exam.paper 的数据：~2 rows (大约)

-- 导出  表 server-exam.paperrule 结构
CREATE TABLE IF NOT EXISTS `paperrule` (
  `ID` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '创建时间',
  `HeadlineID` int(10) unsigned zerofill DEFAULT NULL COMMENT '大标题ID',
  `KnowledgeID` int(10) unsigned zerofill DEFAULT NULL COMMENT '知识点ID',
  `QuestionType` int(10) unsigned zerofill DEFAULT NULL COMMENT '试题类型 1单选 2判断 3多选 4填空 5问答 6代码实训 7拖拽 8连线',
  `QuestionNum` int(10) unsigned zerofill DEFAULT NULL COMMENT '抽题数量',
  `SingleScore` decimal(10,2) unsigned zerofill DEFAULT NULL COMMENT '单题分数',
  `PaperID` int(10) unsigned zerofill DEFAULT NULL COMMENT '试卷ID',
  `PaperRuleState` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '试卷规则状态 1正常 2禁用',
  `SerialNumber` int(5) unsigned zerofill DEFAULT NULL COMMENT '排序',
  `UpdateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='试卷规则';

-- 正在导出表  server-exam.paperrule 的数据：~28 rows (大约)

-- 导出  表 server-exam.practice 结构
CREATE TABLE IF NOT EXISTS `practice` (
  `ID` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '创建时间',
  `QuestionTitle` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '题目',
  `QuestionCode` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '试题代码',
  `QuestionType` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '试题类型 1单选 2判断 3多选 4填空 5问答 6代码实训 7拖拽题 8连线题',
  `Marking` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '人工阅卷 1否 2是',
  `KnowledgeID` int(10) unsigned zerofill DEFAULT NULL COMMENT '知识点ID',
  `Description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '试题描述',
  `Attachment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '试题附件',
  `UpdateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '更新时间',
  `Score` decimal(10,2) unsigned zerofill DEFAULT NULL COMMENT '额定分数',
  `ExamineeID` int(10) unsigned zerofill DEFAULT NULL COMMENT '考生ID',
  `HeadlineContent` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '大标题内容',
  `ExamineeTokenID` int(10) unsigned zerofill DEFAULT NULL COMMENT '考生TokenID',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='练习题';

-- 正在导出表  server-exam.practice 的数据：~0 rows (大约)

-- 导出  表 server-exam.practicesolution 结构
CREATE TABLE IF NOT EXISTS `practicesolution` (
  `ID` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '创建时间',
  `PracticeID` int(10) unsigned zerofill DEFAULT NULL COMMENT '练习题ID',
  `Option` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '试题选项',
  `OptionAttachment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '选项附件',
  `CorrectAnswer` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '正确答案 1错误 2正确',
  `CorrectItem` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '答案项',
  `ScoreRatio` decimal(10,2) unsigned zerofill DEFAULT NULL COMMENT '得分比例',
  `Position` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '拖拽题/连线题 展示位置 1左 2右',
  `UpdateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '更新时间',
  `CandidateAnswer` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '考生答案',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='练习题选项';

-- 正在导出表  server-exam.practicesolution 的数据：~0 rows (大约)

-- 导出  表 server-exam.question 结构
CREATE TABLE IF NOT EXISTS `question` (
  `ID` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '创建时间',
  `QuestionTitle` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '标题',
  `QuestionCode` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '标题代码',
  `QuestionType` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '试题类型 1单选 2判断 3多选 4填空 5问答 6代码实训 7拖拽 8连线',
  `QuestionState` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '试题状态 1正常 2禁用',
  `Marking` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '人工阅卷 1否 2是',
  `KnowledgeID` int(1) unsigned zerofill DEFAULT NULL COMMENT '知识点ID',
  `Description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '试题描述',
  `Attachment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '试题附件',
  `UpdateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '更新时间',
  `Language` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '计算机语言',
  `LanguageVersion` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '计算机语言版本',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='试题';

-- 正在导出表  server-exam.question 的数据：~17 rows (大约)

-- 导出  表 server-exam.questionsolution 结构
CREATE TABLE IF NOT EXISTS `questionsolution` (
  `ID` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '创建时间',
  `QuestionID` int(10) unsigned zerofill DEFAULT NULL COMMENT '试题ID',
  `Option` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '试题选项',
  `OptionAttachment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '试题附件',
  `CorrectAnswer` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '正确答案 1错误 2正确',
  `CorrectItem` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '答案项',
  `ScoreRatio` decimal(10,2) unsigned zerofill DEFAULT NULL COMMENT '得分比例',
  `Position` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '拖拽题/连线题 展示位置 1左 2右',
  `UpdateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='试题选项';

-- 正在导出表  server-exam.questionsolution 的数据：~45 rows (大约)

-- 导出  表 server-exam.scantron 结构
CREATE TABLE IF NOT EXISTS `scantron` (
  `ID` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '创建时间',
  `QuestionTitle` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '标题',
  `QuestionCode` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '标题代码',
  `QuestionType` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '试题类型 1单选 2判断 3多选 4填空 5问答 6代码实训 7拖拽题 8连线题',
  `Marking` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '人工阅卷 1否 2是',
  `KnowledgeID` int(10) unsigned zerofill DEFAULT NULL COMMENT '知识点ID',
  `Description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '试题描述',
  `Attachment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '试题附件',
  `UpdateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '更新时间',
  `Score` decimal(10,2) unsigned zerofill DEFAULT NULL COMMENT '额定分数',
  `ExamID` int(10) unsigned zerofill DEFAULT NULL COMMENT '报名ID',
  `HeadlineContent` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '大标题内容',
  `Right` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '是否正确作答 1 否 2 是',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='答题卡';

-- 正在导出表  server-exam.scantron 的数据：~0 rows (大约)

-- 导出  表 server-exam.scantronhistory 结构
CREATE TABLE IF NOT EXISTS `scantronhistory` (
  `ID` int(10) unsigned zerofill NOT NULL,
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '创建时间',
  `QuestionTitle` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '标题',
  `QuestionCode` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '标题代码',
  `QuestionType` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '试题类型 1单选 2判断 3多选 4填空 5问答 6代码实训 7拖拽题 8连线题',
  `Marking` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '人工阅卷 1否 2是',
  `KnowledgeID` int(10) unsigned zerofill DEFAULT NULL COMMENT '知识点ID',
  `Description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '试题描述',
  `Attachment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '试题附件',
  `UpdateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '更新时间',
  `Score` decimal(10,2) unsigned zerofill DEFAULT NULL COMMENT '额定分数',
  `ExamID` int(10) unsigned zerofill DEFAULT NULL COMMENT '报名ID',
  `HeadlineContent` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '大标题内容',
  `Right` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '是否正确作答 1 否 2 是',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='历史答题卡';

-- 正在导出表  server-exam.scantronhistory 的数据：~0 rows (大约)

-- 导出  表 server-exam.scantronsolution 结构
CREATE TABLE IF NOT EXISTS `scantronsolution` (
  `ID` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '创建时间',
  `ScantronID` int(10) unsigned zerofill DEFAULT NULL COMMENT '试题ID',
  `Option` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '试题选项',
  `OptionAttachment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '试题附件',
  `CorrectAnswer` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '正确答案 1错误 2正确',
  `CorrectItem` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '答案项',
  `ScoreRatio` decimal(10,2) unsigned zerofill DEFAULT NULL COMMENT '得分比例',
  `Position` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '拖拽题/连线题 展示位置 1左 2右',
  `UpdateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '更新时间',
  `CandidateAnswer` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '考生答案',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='答题卡选项';

-- 正在导出表  server-exam.scantronsolution 的数据：~0 rows (大约)

-- 导出  表 server-exam.scantronsolutionhistory 结构
CREATE TABLE IF NOT EXISTS `scantronsolutionhistory` (
  `ID` int(10) unsigned zerofill NOT NULL,
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '创建时间',
  `ScantronID` int(10) unsigned zerofill DEFAULT NULL COMMENT '试题ID',
  `Option` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '试题选项',
  `OptionAttachment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '试题附件',
  `CorrectAnswer` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '正确答案 1错误 2正确',
  `CorrectItem` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '答案项',
  `ScoreRatio` decimal(10,2) unsigned zerofill DEFAULT NULL COMMENT '得分比例',
  `Position` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '拖拽题/连线题 展示位置 1左 2右',
  `UpdateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '更新时间',
  `CandidateAnswer` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '考生答案',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='历史答题卡选项';

-- 正在导出表  server-exam.scantronsolutionhistory 的数据：~0 rows (大约)

-- 导出  表 server-exam.subject 结构
CREATE TABLE IF NOT EXISTS `subject` (
  `ID` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '创建时间',
  `SubjectName` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '科目名称',
  `SubjectCode` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '科目代码',
  `SubjectState` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '科目状态 1正常 2禁用',
  `UpdateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='科目';

-- 正在导出表  server-exam.subject 的数据：~0 rows (大约)

-- 导出  表 server-exam.sysconf 结构
CREATE TABLE IF NOT EXISTS `sysconf` (
  `ID` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '创建时间',
  `Type` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '配置类型',
  `Key` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '配置KEY',
  `Value` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '配置Value',
  `Description` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '配置描述',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统配置';

-- 正在导出表  server-exam.sysconf 的数据：~0 rows (大约)

-- 导出  表 server-exam.syslog 结构
CREATE TABLE IF NOT EXISTS `syslog` (
  `ID` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '创建时间',
  `Type` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '日志类型 1操作 2登录',
  `ManagerID` int(10) unsigned zerofill DEFAULT NULL COMMENT '管理员ID',
  `Description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '描述信息',
  `IP` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'IP地址',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统日志';

-- 正在导出表  server-exam.syslog 的数据：~0 rows (大约)

-- 导出  表 server-exam.teacher 结构
CREATE TABLE IF NOT EXISTS `teacher` (
  `ID` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '创建时间',
  `Account` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '账号',
  `Password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '密码',
  `Name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '名称',
  `State` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '状态 1正常 2禁用',
  `UpdateTime` int(10) unsigned zerofill DEFAULT NULL COMMENT '更新时间',
  `Token` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'token',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='教师';

-- 正在导出表  server-exam.teacher 的数据：~0 rows (大约)

-- 导出  表 server-exam.teacherclass 结构
CREATE TABLE IF NOT EXISTS `teacherclass` (
  `ID` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `CreateTime` int(10) unsigned zerofill DEFAULT NULL,
  `TeacherID` int(10) unsigned zerofill DEFAULT NULL,
  `ClassID` int(10) unsigned zerofill DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='教师班级对应数据';

-- 正在导出表  server-exam.teacherclass 的数据：~0 rows (大约)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
