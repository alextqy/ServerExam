# -*- coding:utf-8 -*-
from Controller.BaseController import *

PracticeRouter = APIRouter()
PracticePrefix = ''


# 刷题登陆
@PracticeRouter.post('/Sign/In/Practice')
async def SignInPractice(
        request: Request,
        ExamineeNo: str = Form(''),
) -> Result:
    return practiceLogic.SignInPractice(ExamineeNo)


# 随机抽取一道指定类型的试题
@PracticeRouter.post('/New/Practice')
async def NewPractice(
        request: Request,
        Token: str = Form(''),
        QuestionType: int = Form(0),
) -> Result:
    return practiceLogic.NewPractice(Token, QuestionType)


# 获取试题信息
@PracticeRouter.post('/Practice/Info')
async def PracticeInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return practiceLogic.PracticeInfo(Token, ID)


# 答题
@PracticeRouter.post('/Practice/Answer')
async def PracticeAnswer(
        request: Request,
        Token: str = Form(''),
        PracticeID: int = Form(0),
        ID: int = Form(0),
        Answer: str = Form(''),
) -> Result:
    return practiceLogic.PracticeAnswer(Token, PracticeID, ID, Answer)


# 验证
@PracticeRouter.post('/Grade/The/Practice')
async def GradeThePractice(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return practiceLogic.GradeThePractice(Token, ID)


# 删除刷题数据
@PracticeRouter.post('/Practice/Delete')
async def PracticeDelete(
        request: Request,
        ID: int = Form(0),
) -> Result:
    return practiceLogic.PracticeDeleteAction(ID)
