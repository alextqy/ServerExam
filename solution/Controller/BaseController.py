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
from Logic.HeadlineLogic import HeadlineLogic
from Logic.QuestionLogic import QuestionLogic
from Logic.ExamineeLogic import ExamineeLogic

managerLogic = ManagerLogic()
subjectLogic = SubjectLogic()
knowledgeLogic = KnowledgeLogic()
paperLogic = PaperLogic()
headlineLogic = HeadlineLogic()
questionLogic = QuestionLogic()
# examineeLogic = ExamineeLogic()