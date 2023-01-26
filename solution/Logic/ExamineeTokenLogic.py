# -*- coding:utf-8 -*-
from Logic.BaseLogic import *


class ExamineeTokenLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    # 获取当前考生的报名列表
    def SignInStudentID(self, Account: str):
        result = Result()
        _dbsession = DBsession()
        if Account == '':
            result.Memo = self._lang.WrongAccount
        else:
            ExamineeData: ExamineeEntity = self._examineeModel.FindExamineeNo(_dbsession, Account)
            if ExamineeData is None:
                result.Memo = self._lang.ExamineeDataDoesNotExist
            else:
                ExamInfoList: list = self._examInfoModel.FindExamineeID(_dbsession, ExamineeData.ID)
                for i in ExamInfoList[:]:
                    ExamInfoData: ExamInfoEntity = i
                    if ExamInfoData.EndTime > 0 and self._common.Time() >= ExamInfoData.EndTime:
                        ExamInfoList.remove(ExamInfoData)
                result.Data = ExamInfoList
                result.State = True
        _dbsession.close()
        return result

    def SignInAdmissionTicket(self, ClientHost: str, ExamNo: str):
        result = Result()
        _dbsession = DBsession()
        if ExamNo == '':
            result.Memo = self._lang.WrongExamNo
        else:
            ExamInfoData: ExamInfoEntity = self._examInfoModel.FindExamNo(_dbsession, ExamNo)
            if ExamInfoData is None:
                result.Memo = self._lang.ExamDataDoesNotExist
            else:
                result = self.PostLoginOperationAction(ClientHost, ExamInfoData.ID)
        _dbsession.close()
        return result

    def PostLoginOperationAction(self, ClientHost: str, ExamInfoID: int):
        result = Result()
        _dbsession = DBsession()
        if ExamInfoID <= 0:
            result.Memo = self._lang.RegistrationDataError
        else:
            _dbsession.begin_nested()

            # 获取报名数据
            ExamInfoData: ExamInfoEntity = self._examInfoModel.Find(_dbsession, ExamInfoID)
            if ExamInfoData is None:
                result.Memo = self._lang.ExamDataDoesNotExist
            elif ExamInfoData.ExamState != 2:
                result.Memo = self._lang.RegistrationDataError
            elif ExamInfoData.EndTime > 0 and self._common.Time() >= ExamInfoData.EndTime:
                result.Memo = self._lang.TimeOut
            else:
                # 删除相同报名Token
                CheckToken: ExamineeTokenEntity = self._examineeTokenModel.FindExamID(_dbsession, ExamInfoData.ID)
                if CheckToken is not None:
                    DelInfo: Result = self._examineeTokenModel.Delete(_dbsession, CheckToken.ID)
                    if DelInfo.State == False:
                        return result

                SignInTime: str = self._common.Time()

                # 生成考生Token
                ExamineeTokenData = ExamineeTokenEntity()
                ExamineeTokenData.CreateTime = SignInTime
                ExamineeTokenData.ExamID = ExamInfoData.ID
                ExamineeTokenData.Token = self._common.GenerateToken()
                AddInfo: Result = self._examineeTokenModel.Insert(_dbsession, ExamineeTokenData)
                if AddInfo.State == False:
                    result.Memo = AddInfo.Memo
                    return result

                # 修改报名考试起止时间
                try:
                    ExamInfoData.StartTime = SignInTime
                    ExamInfoData.EndTime = SignInTime + ExamInfoData.ExamDuration
                    ExamInfoData.StartState = 2
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                # 记录日志
                Desc = 'examinee login exam No.:' + ExamInfoData.ExamNo
                if self.LogExamAction(_dbsession, 2, ExamInfoData.ExamNo, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.Data = ExamineeTokenData.Token
                result.State = True
        _dbsession.close()
        return result

    def ExamScantronList(self, Token: str):
        result = Result()
        _dbsession = DBsession()
        ExamID: int = self.ExamineeTokenValidation(_dbsession, Token)
        if ExamID == 0:
            result.Memo = self._lang.WrongToken
        else:
            ScantronData: list = self._scantronModel.FindExamID(_dbsession, ExamID)
            result.State = True
            result.Data = ScantronData
        _dbsession.close()
        return result

    def ExamScantronSolutionInfo(self, Token: str, ID: int):
        result = Result()
        _dbsession = DBsession()
        ExamID: int = self.ExamineeTokenValidation(_dbsession, Token)
        if ExamID == 0:
            result.Memo = self._lang.WrongToken
        elif ID <= 0:
            result.Memo = self._lang.WrongToken
        else:
            ScantronData: ScantronEntity = self._scantronModel.Find(_dbsession, ID)
            if ScantronData is None:
                result.Memo = self._lang.WrongData
            elif ScantronData.QuestionType >= 4 and ScantronData.QuestionType <= 6:
                result.State = True
                return result
            else:
                ScantronSolutionList: list = self._scantronSolutionModel.FindScantronID(_dbsession, ScantronData.ID)
                if len(ScantronSolutionList) > 0:
                    for i in ScantronSolutionList:
                        ScantronSolutionData: ScantronSolutionEntity = i
                        ScantronSolutionData.CorrectAnswer = 0
                        ScantronSolutionData.CorrectItem = ''
                    ScantronData.ScantronSolutionList = ScantronSolutionList
                    result.Data = ScantronData
                result.State = True
        _dbsession.close()
        return result

    def ExamAnswer(self, Token: str, ScantronID: int, ID: int, Answer: str = ''):
        result = Result()
        _dbsession = DBsession()
        ExamID: int = self.ExamineeTokenValidation(_dbsession, Token)
        if ExamID == 0:
            result.Memo = self._lang.WrongToken
        else:
            if ScantronID <= 0:
                result.State = False
            elif ID <= 0:
                result.State = False
            else:
                ScantronData: ScantronEntity = self._scantronModel.Find(_dbsession, ScantronID)
                if ScantronData is None:
                    result.Memo = self._lang.WrongData
                elif ScantronData.ExamID != ExamID:
                    result.Memo = self._lang.PermissionDenied
                else:
                    _dbsession.begin_nested()

                    # 获取当前试题选项列表
                    ScantronSolutionDataList: list = self._scantronSolutionModel.FindScantronID(_dbsession, ScantronData.ID)
                    if len(ScantronSolutionDataList) == 0:
                        result.Memo = self._lang.WrongData
                        return result
                    for i in ScantronSolutionDataList:
                        ScantronSolutionData: ScantronSolutionEntity = i
                        # 单选/判断题 选项 =======================================================================================
                        # 单选判断ID不能输入错误 否侧全为False
                        if ScantronData.QuestionType >= 1 and ScantronData.QuestionType <= 2:
                            if ScantronSolutionData.ID == ID:
                                ScantronSolutionData.CandidateAnswer = 'True'
                            else:
                                ScantronSolutionData.CandidateAnswer = 'False'
                        # 多选题选项 =======================================================================================
                        # 多选题Answer不为空则为选择
                        elif ScantronData.QuestionType == 3 and ScantronSolutionData.ID == ID:
                            if Answer != '':
                                Answer = 'True'
                            else:
                                Answer = ''
                            ScantronSolutionData.CandidateAnswer = Answer
                        # 填空/问答/实训 题选项 =======================================================================================
                        elif ScantronData.QuestionType >= 4 and ScantronData.QuestionType <= 6 and ScantronSolutionData.ID == ID:
                            ScantronSolutionData.CandidateAnswer = Answer
                        # 拖拽选项 =======================================================================================
                        elif ScantronData.QuestionType == 7 and ScantronSolutionData.ID == ID:
                            if ScantronSolutionData.Position != 2:
                                result.Memo = self._lang.WrongData
                                return result
                            else:
                                if Answer != '':
                                    if int(Answer) == ID:
                                        result.Memo = self._lang.WrongData
                                        return result
                                    ScantronSolutionDataSub: ScantronSolutionEntity = self._scantronSolutionModel.Find(_dbsession, int(Answer))
                                    if ScantronSolutionDataSub is None:
                                        result.Memo = self._lang.WrongData
                                        return result
                                    if ScantronSolutionDataSub.ScantronID != ScantronSolutionData.ScantronID:
                                        result.Memo = self._lang.WrongData
                                        return result
                                    if ScantronSolutionDataSub.Position == 2:
                                        result.Memo = self._lang.WrongData
                                        return result
                                ScantronSolutionData.CandidateAnswer = Answer
                        # 连线选项 =======================================================================================
                        elif ScantronData.QuestionType == 8 and ScantronSolutionData.ID == ID:
                            if ScantronSolutionData.Position != 2:
                                result.Memo = self._lang.WrongData
                                return result
                            else:
                                if Answer != '':
                                    AnswerList: list = list(set(Answer.split(',')))
                                    if len(AnswerList) > 0:
                                        for i in AnswerList:
                                            AnswerID: int = int(i)
                                            ScantronSolutionDataSub: ScantronSolutionEntity = self._scantronSolutionModel.Find(_dbsession, AnswerID)
                                            if ScantronSolutionDataSub is None:
                                                result.Memo = self._lang.WrongData
                                                return result
                                            if ScantronSolutionDataSub.ScantronID != ScantronSolutionData.ScantronID:
                                                result.Memo = self._lang.WrongData
                                                return result
                                            if ScantronSolutionDataSub.Position == 2:
                                                result.Memo = self._lang.WrongData
                                                return result
                                    ScantronSolutionData.CandidateAnswer = ','.join(AnswerList)
                        else:
                            continue
                        ScantronSolutionData.UpdateTime = self._common.Time()
                        _dbsession.commit()

                    _dbsession.commit()
                    result.State = True
        _dbsession.close()
        return result

    def EndTheExam(self, ClientHost: str, Token: str):
        result = Result()
        _dbsession = DBsession()
        ExamID: int = self.ExamineeTokenValidation(_dbsession, Token)
        if ExamID == 0:
            result.Memo = self._lang.WrongToken
        else:
            ExamInfoData: ExamInfoEntity = self._examInfoModel.Find(_dbsession, ExamID)
            if ExamInfoData is None:
                result.Memo = self._lang.WrongData
            else:
                # 结束报名
                try:
                    ExamInfoData.ExamState = 3
                    ExamInfoData.ActualDuration = self._common.Time() - ExamInfoData.StartTime
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                # 删除对应Token
                DelInfo: Result = self._examineeTokenModel.DeleteToken(_dbsession, Token)
                if DelInfo.State == False:
                    result.Memo = DelInfo.Memo
                    return result

                # 记录日志
                Desc = 'examinee end the exam No.:' + ExamInfoData.ExamNo
                if self.LogExamAction(_dbsession, 2, ExamInfoData.ExamNo, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result