from Controller.BaseController import *

QuestionRouter = APIRouter()
QuestionPrefix = ''


# 新建试题
@QuestionRouter.post('/New/Question')
async def NewQuestion(request: Request, Token: str = Form(''), QuestionTitle: str = Form(''), QuestionType: int = Form(0), KnowledgeID: int = Form(0), Description: str = Form('')) -> Result:
    Token = Token.strip()
    QuestionTitle = QuestionTitle.strip()
    Description = Description.strip()
    return questionLogic.NewQuestion(request.client.host, Token, QuestionTitle, QuestionType, KnowledgeID, Description)


# 上传试题附件
@QuestionRouter.post('/Question/Attachment')
async def QuestionAttachment(request: Request, Token: str = Form(''), ID: int = Form(0), Attachment: UploadFile = File(...)) -> Result:
    Token = Token.strip()
    Contents: bytes = await Attachment.read()
    return questionLogic.QuestionAttachment(request.client.host, Token, ID, Attachment.content_type.split('/')[1], Contents)