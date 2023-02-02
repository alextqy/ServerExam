# -*- coding:utf-8 -*-
from typing import List, Dict, Tuple

from Service.Cache import *
from Service.Common import *
from Service.Database import *
from Service.FileHelper import *
from Service.Lang import *
from Service.UDPTool import *
from Service.RedisHelper import *

from Entity.BaseEntity import DBsession
from Entity.ClassEntity import ClassEntity
from Entity.ExamineeEntity import ExamineeEntity
from Entity.ExamineeTokenEntity import ExamineeTokenEntity
from Entity.ExamInfoEntity import ExamInfoEntity
from Entity.ExamInfoHistoryEntity import ExamInfoHistoryEntity
from Entity.ExamLogEntity import ExamLogEntity
from Entity.HeadlineEntity import HeadlineEntity
from Entity.KnowledgeEntity import KnowledgeEntity
from Entity.ManagerEntity import ManagerEntity
from Entity.PaperEntity import PaperEntity
from Entity.PaperRuleEntity import PaperRuleEntity
from Entity.PracticeEntity import PracticeEntity
from Entity.PracticeSolutionEntity import PracticeSolutionEntity
from Entity.QuestionEntity import QuestionEntity
from Entity.QuestionSolutionEntity import QuestionSolutionEntity
from Entity.ScantronEntity import ScantronEntity
from Entity.ScantronHistoryEntity import ScantronHistoryEntity
from Entity.ScantronSolutionEntity import ScantronSolutionEntity
from Entity.ScantronSolutionHistoryEntity import ScantronSolutionHistoryEntity
from Entity.SubjectEntity import SubjectEntity
from Entity.SysConfEntity import SysConfEntity
from Entity.SysLogEntity import SysLogEntity
from Entity.TeacherClassEntity import TeacherClassEntity
from Entity.TeacherEntity import TeacherEntity

from Model.ClassModel import ClassModel
from Model.ExamineeModel import ExamineeModel
from Model.ExamineeTokenModel import ExamineeTokenModel
from Model.ExamInfoModel import ExamInfoModel
from Model.ExamInfoHistoryModel import ExamInfoHistoryModel
from Model.ExamLogModel import ExamLogModel
from Model.HeadlineModel import HeadlineModel
from Model.KnowledgeModel import KnowledgeModel
from Model.ManagerModel import ManagerModel
from Model.PaperModel import PaperModel
from Model.PaperRuleModel import PaperRuleModel
from Model.PracticeModel import PracticeModel
from Model.PracticeSolutionModel import PracticeSolutionModel
from Model.QuestionModel import QuestionModel
from Model.QuestionSolutionModel import QuestionSolutionModel
from Model.ScantronModel import ScantronModel
from Model.ScantronHistoryModel import ScantronHistoryModel
from Model.ScantronSolutionModel import ScantronSolutionModel
from Model.ScantronSolutionHistoryModel import ScantronSolutionHistoryModel
from Model.SubjectModel import SubjectModel
from Model.SysConfModel import SysConfModel
from Model.SysLogModel import SysLogModel
from Model.TeacherClassModel import TeacherClassModel
from Model.TeacherModel import TeacherModel


class BaseLogic:
    _cache: Cache = Cache()
    _common: Common = Common()
    _file: FileHelper = FileHelper()
    _lang: Lang = Lang()
    _udp: UDPTool = UDPTool()
    _redis: RedisHelper = RedisHelper()

    _classModel = ClassModel()
    _examineeModel = ExamineeModel()
    _examineeTokenModel = ExamineeTokenModel()
    _examInfoModel = ExamInfoModel()
    _examInfoHistoryModel = ExamInfoHistoryModel()
    _examLogModel = ExamLogModel()
    _headlineModel = HeadlineModel()
    _knowledgeModel = KnowledgeModel()
    _managerModel = ManagerModel()
    _paperModel = PaperModel()
    _paperRuleModel = PaperRuleModel()
    _practiceModel = PracticeModel()
    _practiceSolutionModel = PracticeSolutionModel()
    _questionModel = QuestionModel()
    _questionSolutionModel = QuestionSolutionModel()
    _scantronModel = ScantronModel()
    _scantronHistoryModel = ScantronHistoryModel()
    _scantronSolutionModel = ScantronSolutionModel()
    _scantronSolutionHistoryModel = ScantronSolutionHistoryModel()
    _subjectModel = SubjectModel()
    _sysConfModel = SysConfModel()
    _sysLogModel = SysLogModel()
    _teacherClassModel = TeacherClassModel()
    _teacherModel = TeacherModel()

    _rootPath = path[0] + '/'

    def __init__(self):
        super().__init__()

    def PermissionValidation(self, _dbsession: DBsession, Token: str) -> int:
        ManagerData: ManagerEntity = self._managerModel.FindToken(_dbsession, Token)
        if ManagerData is None:
            return 0
        elif ManagerData.Permission < 9:
            return 0
        return ManagerData.ID

    def TeacherPermissionValidation(self, _dbsession: DBsession, Token: str) -> int:
        TeacherData: TeacherEntity = self._teacherModel.FindToken(_dbsession, Token)
        if TeacherData is None:
            return 0
        return TeacherData.ID

    def ExamineeTokenValidation(self, _dbsession: DBsession, Token: str) -> int:
        ExamineeTokenData: ExamineeTokenEntity = self._examineeTokenModel.FindToken(_dbsession, Token)
        if ExamineeTokenData is None:
            return 0
        else:
            ExamInfoData: ExamInfoEntity = self._examInfoModel.Find(_dbsession, ExamineeTokenData.ExamID)
            if ExamInfoData is None:
                self._examineeTokenModel.Delete(_dbsession, ExamineeTokenData.ID)
                return 0
            elif ExamInfoData.ExamState != 2:
                self._examineeTokenModel.Delete(_dbsession, ExamineeTokenData.ID)
                return 0
            elif self._common.Time() >= ExamInfoData.EndTime:
                self._examineeTokenModel.Delete(_dbsession, ExamineeTokenData.ID)
                return 0
            else:
                return ExamineeTokenData.ExamID

    def PracticeValidation(self, _dbsession: DBsession, Token: str) -> int:
        ExamineeTokenData: ExamineeTokenEntity = self._examineeTokenModel.FindToken(_dbsession, Token)
        if ExamineeTokenData is None:
            return 0
        elif ExamineeTokenData.ExamID != 0:
            return 0
        else:
            return ExamineeTokenData.ID

    def LogSysAction(self, _dbsession: DBsession, Type: int, ManagerID: int, Description: str, IP: str) -> bool:
        LogData = SysLogEntity()
        LogData.Type = Type
        LogData.ManagerID = ManagerID
        LogData.Description = Description
        LogData.IP = IP
        result: Result = self._sysLogModel.Insert(_dbsession, LogData)
        if result.State == True:
            return True
        else:
            return False

    def LogExamAction(self, _dbsession: DBsession, Type: int, ExamNo: str, Description: str, IP: str) -> bool:
        LogData = ExamLogEntity()
        LogData.Type = Type
        LogData.ExamNo = ExamNo
        LogData.Description = Description
        LogData.IP = IP
        result: Result = self._examLogModel.Insert(_dbsession, LogData)
        if result.State == True:
            return True
        else:
            return False