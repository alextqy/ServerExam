from Service.Cache import *
from Service.Common import *
from Service.Database import *
from Service.File import *
from Service.Lang import *
from Service.UDPTool import *

from Entity.BaseEntity import DBsession
from Entity.ExamineeEntity import ExamineeEntity
from Entity.ExamineeTokenEntity import ExamineeTokenEntity
from Entity.ExamInfoEntity import ExamInfoEntity
from Entity.ExamLogEntity import ExamLogEntity
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

from Model.ExamineeModel import ExamineeModel


class BaseLogic:
    _cache: Cache = Cache()
    _common: Common = Common()
    _file: File = File()
    _lang: Lang = Lang()
    _udp: UDPTool = UDPTool()

    _examineemodel = ExamineeModel()

    def __init__(self):
        super().__init__()