from Service.Cache import *
from Service.Common import *
from Service.Database import *
from Service.FileHelper import *
from Service.Lang import *
from Service.UDPTool import *

from Logic.ManagerLogic import ManagerLogic
from Logic.SubjectLogic import SubjectLogic
from Logic.PaperLogic import PaperLogic
from Logic.PaperRuleLogic import PaperRuleLogic
from Logic.KnowledgeLogic import KnowledgeLogic
from Logic.HeadlineLogic import HeadlineLogic
from Logic.QuestionLogic import QuestionLogic
from Logic.QuestionSolutionLogic import QuestionSolutionLogic
from Logic.ClassLogic import ClassLogic
from Logic.ExamineeLogic import ExamineeLogic

managerLogic = ManagerLogic()
subjectLogic = SubjectLogic()
paperLogic = PaperLogic()
paperRuleLogic = PaperRuleLogic()
knowledgeLogic = KnowledgeLogic()
headlineLogic = HeadlineLogic()
questionLogic = QuestionLogic()
questionSolutionLogic = QuestionSolutionLogic()
classLogic = ClassLogic()

examineeLogic = ExamineeLogic()