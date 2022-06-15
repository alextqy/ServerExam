# -*- coding:utf-8 -*-
from Service.BaseService import *
from Service.Common import *

_common = Common()
ConfigObj: dict = _common.ReadJsonFile(path[0] + '/config.json')


class Lang(BaseService):

    def __init__(self):
        super().__init__()
        self.Type = str.lower(ConfigObj["Lang"])

        # 英文
        if self.Type == "en":
            self.WrongToken = 'wrong token'
            self.PermissionDenied = 'permission denied'
            self.WrongClassName = 'wrong class name'
            self.ClassDataAlreadyExists = 'class data already exists'
            self.LoggingFailed = 'logging failed'
            self.WrongID = 'wrong ID'
            self.ClassDataError = 'class data error'
            self.WrongExamineeNo = 'wrong examinee No.'
            self.WrongName = 'wrong name'
            self.WrongClassID = 'wrong class ID'
            self.ExamineeNoDataAlreadyExists = 'examinee No. data already exists'
            self.ClassDataDoesNotExist = 'class data does not exist'
            self.ExamineeDataError = 'examinee data error'
            self.WrongAccount = 'wrong account'
            self.ExamineeDataDoesNotExist = 'examinee data does not exist'
            self.ExamDataDoesNotExist = 'exam data does not exist'
            self.WrongSubjectName = 'wrong subject name'
            self.WrongExamNo = 'wrong exam No.'
            self.WrongExamType = 'wrong exam type'
            self.SubjectDataError = 'subject data error'
            self.SubjectDataIsDisabled = 'subject data is disabled'
            self.AlreadyRegisteredForTheSameSubject = 'already registered for the same subject'
            self.ExamNoDataAlreadyExists = 'exam No. data already exists'
            self.ExamDataError = 'exam data error'
            self.ExamCompleted = 'exam completed'
            self.QuestionDataAlreadyExists = 'question data already exists'
            self.ExamDataDisabled = 'exam data disabled'
            self.SubjectDataDoesNotExist = 'subject data does not exist'
            self.PaperDataDoesNotExist = 'paper data does not exist'
            self.HeadlineDataError = 'headline data error'
            self.ExamPaperRulesError = 'exam paper rules error'
            self.NotEnoughQuestions = 'not enough questions'
            self.WrongQuestionOptions = 'wrong question options'
            self.HasNotYetTakenTheExam = 'has not yet taken the exam'
            self.ExamLogDataError = 'exam log data error'
            self.WrongContent = 'wrong content'
            self.HeadlineDataAlreadyExists = 'headline data already exists'

            self.Account = "Account"
            self.Name = "Name"
            self.PWD = "Password"
            self.IP = "IP"

        # 中文简体
        elif self.Type == "zh-cn":
            self.WrongToken = '登陆令牌有误'
            self.PermissionDenied = 'permission denied'
            self.WrongClassName = 'wrong class name'
            self.ClassDataAlreadyExists = 'class data already exists'
            self.LoggingFailed = 'logging failed'
            self.WrongID = 'wrong ID'
            self.ClassDataError = 'class data error'
            self.WrongExamineeNo = 'wrong examinee No.'
            self.WrongName = 'wrong name'
            self.WrongClassID = 'wrong class ID'
            self.ExamineeNoDataAlreadyExists = 'examinee No. data already exists'
            self.ClassDataDoesNotExist = 'class data does not exist'
            self.ExamineeDataError = 'examinee data error'
            self.WrongAccount = 'wrong account'
            self.ExamineeDataDoesNotExist = 'examinee data does not exist'
            self.ExamDataDoesNotExist = 'exam data does not exist'
            self.WrongSubjectName = 'wrong subject name'
            self.WrongExamNo = 'wrong exam No.'
            self.WrongExamType = 'wrong exam type'
            self.SubjectDataError = 'subject data error'
            self.SubjectDataIsDisabled = 'subject data is disabled'
            self.AlreadyRegisteredForTheSameSubject = 'already registered for the same subject'
            self.ExamNoDataAlreadyExists = 'exam No. data already exists'
            self.ExamDataError = 'exam data error'
            self.ExamCompleted = 'exam completed'
            self.QuestionDataAlreadyExists = 'question data already exists'
            self.ExamDataDisabled = 'exam data disabled'
            self.SubjectDataDoesNotExist = 'subject data does not exist'
            self.PaperDataDoesNotExist = 'paper data does not exist'
            self.HeadlineDataError = 'headline data error'
            self.ExamPaperRulesError = 'exam paper rules error'
            self.NotEnoughQuestions = 'not enough questions'
            self.WrongQuestionOptions = 'wrong question options'
            self.HasNotYetTakenTheExam = ' has not yet taken the exam'
            self.ExamLogDataError = 'exam log data error'
            self.WrongContent = 'wrong content'
            self.HeadlineDataAlreadyExists = 'headline data already exists'

            self.Account = "账号"
            self.Name = "姓名"
            self.PWD = "密码"
            self.IP = "IP"

        # 默认
        else:
            self.WrongToken = ''

            self.Account = ""
            self.Name = ""
            self.PWD = ""
            self.IP = ""