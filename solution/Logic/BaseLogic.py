from Service.Cache import *
from Service.Common import *
from Service.Database import *
from Service.FileHelper import *
from Service.Lang import *
from Service.UDPTool import *

from Entity.BaseEntity import DBsession
from Entity.ClassEntity import ClassEntity
from Entity.ExamineeEntity import ExamineeEntity
from Entity.ExamineeTokenEntity import ExamineeTokenEntity
from Entity.ExamInfoEntity import ExamInfoEntity
from Entity.ExamLogEntity import ExamLogEntity
from Entity.ExerciseEntity import ExerciseEntity
from Entity.ExerciseSolutionEntity import ExerciseSolutionEntity
from Entity.HeadlineEntity import HeadlineEntity
from Entity.KnowledgeEntity import KnowledgeEntity
from Entity.ManagerEntity import ManagerEntity
from Entity.PaperEntity import PaperEntity
from Entity.PaperRuleEntity import PaperRuleEntity
from Entity.QuestionEntity import QuestionEntity
from Entity.QuestionSolutionEntity import QuestionSolutionEntity
from Entity.ScantronEntity import ScantronEntity
from Entity.ScantronHistoryEntity import ScantronHistoryEntity
from Entity.ScantronSolutionEntity import ScantronSolutionEntity
from Entity.ScantronSolutionHistoryEntity import ScantronSolutionHistoryEntity
from Entity.SubjectEntity import SubjectEntity
from Entity.SysConfEntity import SysConfEntity
from Entity.SysLogEntity import SysLogEntity
from Entity.TeacherEntity import TeacherEntity

from Model.ClassModel import ClassModel
from Model.ExamineeModel import ExamineeModel
from Model.ExamineeTokenModel import ExamineeTokenModel
from Model.ExamInfoModel import ExamInfoModel
from Model.ExamLogModel import ExamLogModel
from Model.ExerciseModel import ExerciseModel
from Model.ExerciseSolutionModel import ExerciseSolutionModel
from Model.HeadlineModel import HeadlineModel
from Model.KnowledgeModel import KnowledgeModel
from Model.ManagerModel import ManagerModel
from Model.PaperModel import PaperModel
from Model.PaperRuleModel import PaperRuleModel
from Model.QuestionModel import QuestionModel
from Model.QuestionSolutionModel import QuestionSolutionModel
from Model.ScantronModel import ScantronModel
from Model.ScantronHistoryModel import ScantronHistoryModel
from Model.ScantronSolutionModel import ScantronSolutionModel
from Model.ScantronSolutionHistoryModel import ScantronSolutionHistoryModel
from Model.SubjectModel import SubjectModel
from Model.SysConfModel import SysConfModel
from Model.SysLogModel import SysLogModel
from Model.TeacherModel import TeacherModel


class BaseLogic:
    _cache: Cache = Cache()
    _common: Common = Common()
    _file: FileHelper = FileHelper()
    _lang: Lang = Lang()
    _udp: UDPTool = UDPTool()

    _classModel = ClassModel()
    _examineeModel = ExamineeModel()
    _examineeTokenModel = ExamineeTokenModel()
    _examInfoModel = ExamInfoModel()
    _examLogModel = ExamLogModel()
    _exerciseModel = ExerciseModel()
    _exerciseSolutionModel = ExerciseSolutionModel()
    _headlineModel = HeadlineModel()
    _knowledgeModel = KnowledgeModel()
    _managerModel = ManagerModel()
    _paperModel = PaperModel()
    _paperRuleModel = PaperRuleModel()
    _questionModel = QuestionModel()
    _questionSolutionModel = QuestionSolutionModel()
    _scantronModel = ScantronModel()
    _scantronHistoryModel = ScantronHistoryModel()
    _scantronSolutionModel = ScantronSolutionModel()
    _scantronSolutionHistoryModel = ScantronSolutionHistoryModel()
    _subjectModel = SubjectModel()
    _sysConfModel = SysConfModel()
    _sysLogModel = SysLogModel()
    _teacherModel = TeacherModel()

    def __init__(self):
        super().__init__()

    def PermissionValidation(self, _dbsession: DBsession, Token: str) -> int:
        ManagerData: ManagerEntity = self._managerModel.FindToken(_dbsession, Token)
        if ManagerData is None:
            return 0
        elif ManagerData.Permission < 9:
            return 0
        return ManagerData.ID

    def LogSysAction(self, _dbsession: DBsession, Type: int, ManagerID: int, Description: str, IP: str) -> bool:
        if Type <= 0:
            return False
        elif ManagerID <= 0:
            return False
        elif Description == '':
            return False
        elif IP == '':
            return False
        else:
            LogData = SysLogEntity()
            LogData.Type = Type
            LogData.ManagerID = ManagerID
            LogData.Description = Description
            LogData.IP = IP
            result: Result = self._sysLogModel.Insert(_dbsession, LogData)
            if result.Status == True:
                return True
            else:
                return False
