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
) -> Result:
    return questionSolutionLogic.NewQuestionSolution(request.client.host, Token.strip(), QuestionID, Option.strip(), CorrectAnswer, CorrectItem, ScoreRatio, Position)


# 上传试题选项附件
@QuestionSolutionRouter.post('/Question/Solution/Attachment')
async def QuestionSolutionAttachment(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
        Attachment: UploadFile = File(...),
) -> Result:
    Contents: bytes = await Attachment.read()
    return questionSolutionLogic.QuestionSolutionAttachment(request.client.host, Token.strip(), ID, Attachment.content_type.split('/')[1], Contents)


# 删除试题选项
@QuestionSolutionRouter.post('/Question/Solution/Delete')
async def QuestionSolutionDelete(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return questionSolutionLogic.QuestionSolutionDelete(request.client.host, Token.strip(), ID)


# 试题选项列表
@QuestionSolutionRouter.post('/Question/Solution/List')
async def QuestionSolutionList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        QuestionID: int = Form(0),
) -> ResultList:
    return questionSolutionLogic.QuestionSolutionList(Token.strip(), Page, PageSize, QuestionID)
