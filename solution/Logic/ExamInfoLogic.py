from Logic.BaseLogic import *


class ExamInfoLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewExamInfo(self, ClientHost: str, Token: str, SubjectName: str, ExamNo: str, ExamineeID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif SubjectName == '':
            result.Memo = 'wrong subject name'
        elif ExamNo == '':
            result.Memo = 'wrong exam No.'
        elif ExamineeID <= 0:
            result.Memo = 'wrong examinee ID'
        elif self._subjectModel.FindSubjectCode(_dbsession, SubjectName) is None:
            result.Memo = 'subject data error'
        elif self._examInfoModel.FindExamNo(_dbsession, ExamNo) is not None:
            result.Memo = 'exam No. data already exists'
        elif self._examineeModel.Find(_dbsession, ExamineeID) is None:
            result.Memo = 'examinee data does not exist'
        else:
            # 该考生是否有相同科目的报名且未考试
            CheckData: ExamInfoEntity = self._examInfoModel.CheckExam(_dbsession, ExamineeID, SubjectName)
            if CheckData is not None:
                if CheckData.ExamState < 3:
                    result.Memo = 'already registered for the same subject'
                    return result

            _dbsession.begin_nested()

            ExamInfoData = ExamInfoEntity()
            ExamInfoData.SubjectName = SubjectName
            ExamInfoData.ExamNo = ExamNo
            ExamInfoData.ExamineeID = ExamineeID
            AddInfo: Result = self._examInfoModel.Insert(_dbsession, ExamInfoData)
            if AddInfo.State == False:
                result.Memo = AddInfo.Memo
                return result

            Desc = 'new exam No.:' + ExamNo
            if self.LogSysAction(_dbsession, 1, 0, Desc, ClientHost) == False:
                result.Memo = 'logging failed'
                return result

            _dbsession.commit()
            result.State = True
        return result