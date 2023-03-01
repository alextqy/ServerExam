# -*- coding:utf-8 -*-
from Controller.BaseController import *

QuestionSolutionRouter = APIRouter()
QuestionSolutionPrefix = ''


# 新建试题选项
@QuestionSolutionRouter.post('/New/Question/Solution')
async def NewQuestionSolution(
        request: Request,
        Token: str = Form(''),
        QuestionID: int = Form(0),
        Option: str = Form(''),
        CorrectAnswer: int = Form(0),
        CorrectItem: str = Form(''),
        ScoreRatio: float = Form(0),
        Position: int = Form(0),
):
    return questionSolutionLogic.NewQuestionSolution(request.client.host, Token.strip(), QuestionID, Option.strip(), CorrectAnswer, CorrectItem, ScoreRatio, Position)


# 上传试题选项附件
@QuestionSolutionRouter.post('/Question/Solution/Attachment')
async def QuestionSolutionAttachment(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
        Attachment: UploadFile = File(...),
        ContentType: str = Form(''),
):
    Contents: bytes = await Attachment.read()
    return questionSolutionLogic.QuestionSolutionAttachment(request.client.host, Token.strip(), ID, ContentType, Contents)


# 删除试题选项
@QuestionSolutionRouter.post('/Question/Solution/Delete')
async def QuestionSolutionDelete(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
):
    return questionSolutionLogic.QuestionSolutionDelete(request.client.host, Token.strip(), ID)


# 试题选项列表
@QuestionSolutionRouter.post('/Question/Solution/List')
async def QuestionSolutionList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        QuestionID: int = Form(0),
):
    return questionSolutionLogic.QuestionSolutionList(Token.strip(), Page, PageSize, QuestionID)


# 获取所有试题选项
@QuestionSolutionRouter.post('/Question/Solutions')
async def QuestionSolutions(
        request: Request,
        Token: str = Form(''),
        QuestionID: int = Form(0),
        Position: int = Form(0),
):
    return questionSolutionLogic.QuestionSolutions(Token.strip(), QuestionID, Position)


# 查看附件
@QuestionSolutionRouter.post('/Question/Solution/View/Attachments')
async def QuestionSolutionViewAttachments(
        request: Request,
        Token: str = Form(''),
        FilePath: str = Form(''),
):
    return questionSolutionLogic.QuestionSolutionViewAttachments(Token.strip(), FilePath)


# 删除试题选项
@QuestionSolutionRouter.post('/Set/Score/Ratio')
async def SetScoreRatio(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
        ScoreRatio: float = Form(0),
):
    return questionSolutionLogic.SetScoreRatio(request.client.host, Token.strip(), ID, ScoreRatio)