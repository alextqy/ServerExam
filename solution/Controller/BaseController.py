from Service.Cache import *
from Service.Common import *
from Service.Database import *
from Service.FileHelper import *
from Service.Lang import *
from Service.UDPTool import *

from Logic.ManagerLogic import ManagerLogic
from Logic.SubjectLogic import SubjectLogic
from Logic.KnowledgeLogic import KnowledgeLogic
from Logic.PaperLogic import PaperLogic
from Logic.PaperRuleLogic import PaperRuleLogic
from Logic.HeadlineLogic import HeadlineLogic
from Logic.QuestionLogic import QuestionLogic
from Logic.QuestionSolutionLogic import QuestionSolutionLogic
from Logic.ExamineeLogic import ExamineeLogic

managerLogic = ManagerLogic()
subjectLogic = SubjectLogic()
knowledgeLogic = KnowledgeLogic()
paperLogic = PaperLogic()
paperRuleLogic = PaperRuleLogic()
headlineLogic = HeadlineLogic()
questionLogic = QuestionLogic()
questionSolutionLogic = QuestionSolutionLogic()
examineeLogic = ExamineeLogic()