# -*- coding:utf-8 -*-
from Controller.BaseController import *

QuestionRouter = APIRouter()
QuestionPrefix = ''


# 新建试题
@QuestionRouter.post('/New/Question')
async def NewQuestion(
        request: Request,
        Token: str = Form(''),
        QuestionTitle: str = Form(''),
        QuestionType: int = Form(0),
        KnowledgeID: int = Form(0),
        Description: str = Form(''),
        Language: str = Form(''),
        LanguageVersion: str = Form(''),
) -> Result:
    return questionLogic.NewQuestion(request.client.host, Token.strip(), QuestionTitle.strip(), QuestionType, KnowledgeID, Description.strip(), Language.strip().lower(), LanguageVersion.strip().lower())


# 上传试题附件
@QuestionRouter.post('/Question/Attachment')
async def QuestionAttachment(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
        Attachment: UploadFile = File(...),
) -> Result:
    Contents: bytes = await Attachment.read()
    return questionLogic.QuestionAttachment(request.client.host, Token.strip(), ID, Attachment.content_type, Contents)


# 禁用/启用 试题
@QuestionRouter.post('/Question/Disabled')
async def QuestionDisabled(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return questionLogic.QuestionDisabled(request.client.host, Token.strip(), ID)


# 修改试题信息
@QuestionRouter.post('/Update/Question/Info')
async def UpdateQuestionInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
        QuestionTitle: str = Form(''),
        QuestionType: int = Form(0),
        Description: str = Form(''),
        Language: str = Form(''),
        LanguageVersion: str = Form(''),
) -> Result:
    return questionLogic.UpdateQuestionInfo(request.client.host, Token.strip(), ID, QuestionTitle.strip(), QuestionType, Description.strip(), Language.strip().lower(), LanguageVersion.strip().lower())


# 试题列表
@QuestionRouter.post('/Question/List')
async def QuestionList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        Stext: str = Form(''),
        QuestionType: int = Form(0),
        QuestionState: int = Form(0),
        KnowledgeID: int = Form(0),
) -> ResultList:
    return questionLogic.QuestionList(Token.strip(), Page, PageSize, Stext.strip(), QuestionType, QuestionState, KnowledgeID)


#试题详情
@QuestionRouter.post('/Question/Info')
async def QuestionInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return questionLogic.QuestionInfo(Token.strip(), ID)