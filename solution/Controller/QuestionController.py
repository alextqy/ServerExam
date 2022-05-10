from Controller.BaseController import *

QuestionRouter = APIRouter()
QuestionPrefix = ''


# 新建试题
@QuestionRouter.post('/New/Question')
async def NewQuestion(request: Request, Token: str = Form(''), QuestionTitle: str = Form(''), QuestionType: int = Form(0), KnowledgeID: int = Form(0), Description: str = Form('')) -> Result:
    return questionLogic.NewQuestion(request.client.host, Token.strip(), QuestionTitle.strip(), QuestionType, KnowledgeID, Description.strip())


# 上传试题附件
@QuestionRouter.post('/Question/Attachment')
async def QuestionAttachment(request: Request, Token: str = Form(''), ID: int = Form(0), Attachment: UploadFile = File(...)) -> Result:
    Contents: bytes = await Attachment.read()
    return questionLogic.QuestionAttachment(request.client.host, Token.strip(), ID, Attachment.content_type.split('/')[1], Contents)


# 禁用/启用 试题
@QuestionRouter.post('/Question/Disabled')
async def QuestionDisabled(request: Request, Token: str = Form(''), ID: int = Form(0)) -> Result:
    return questionLogic.QuestionDisabled(request.client.host, Token.strip(), ID)
