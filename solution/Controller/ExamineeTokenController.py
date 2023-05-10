# -*- coding:utf-8 -*-
from Controller.BaseController import *

ExamineeTokenRouter = APIRouter()
ExamineeTokenPrefix = ''


# 学号登录(获取报名列表)
@ExamineeTokenRouter.post('/Sign/In/Student/ID')
async def SignInStudentID(
        request: Request,
        Account: str = Form(''),
):
    return examineeTokenLogic.SignInStudentID(Account.strip())


# 准考证号登录
@ExamineeTokenRouter.post('/Sign/In/Admission/Ticket')
async def SignInAdmissionTicket(
        request: Request,
        ExamNo: str = Form(''),
):
    return examineeTokenLogic.SignInAdmissionTicket(request.client.host, ExamNo.strip())


# 获取答题卡列表
@ExamineeTokenRouter.post('/Exam/Scantron/List')
async def ExamScantronList(
        request: Request,
        Token: str = Form(''),
):
    return examineeTokenLogic.ExamScantronList(Token.strip())


# 获取答题卡选项信息
@ExamineeTokenRouter.post('/Exam/Scantron/Solution/Info')
async def ExamScantronSolutionInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
):
    return examineeTokenLogic.ExamScantronSolutionInfo(Token.strip(), ID)

# 查看附件
@ExamineeTokenRouter.post('/Exam/Scantron/Solution/View/Attachments')
async def ExamScantronSolutionViewAttachments(
        request: Request,
        Token: str = Form(''),
        FilePath: str = Form(''),
):
    return examineeTokenLogic.ExamScantronSolutionViewAttachments(Token.strip(), FilePath)


# 作答
@ExamineeTokenRouter.post('/Exam/Answer')
async def ExamAnswer(
        request: Request,
        Token: str = Form(''),
        ScantronID: int = Form(0),
        ID: int = Form(0),
        Answer: str = Form(''),
):
    return examineeTokenLogic.ExamAnswer(Token.strip(), ScantronID, ID, Answer.strip())


# 结束考试
@ExamineeTokenRouter.post('/End/The/Exam')
async def EndTheExam(
        request: Request,
        Token: str = Form(''),
):
    return examineeTokenLogic.EndTheExam(request.client.host, Token.strip())