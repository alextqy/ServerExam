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

from Model.ManagerModel import ManagerModel
from Model.ExamineeModel import ExamineeModel


class BaseLogic:
    _cache: Cache = Cache()
    _common: Common = Common()
    _file: FileHelper = FileHelper()
    _lang: Lang = Lang()
    _udp: UDPTool = UDPTool()

    _managerModel = ManagerModel()
    _examineeModel = ExamineeModel()

    def __init__(self):
        super().__init__()

    def PermissionValidation(self, _dbsession: DBsession, Token: str) -> ManagerEntity:
        return self._managerModel.FindToken(_dbsession, Token)