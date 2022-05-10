from Controller.BaseController import *

QuestionRouter = APIRouter()
QuestionPrefix = ''


# 新建科目
@QuestionRouter.post('/New/Question')
async def NewQuestion(request: Request, Token: str = Form(''), QuestionTitle: str = Form(''), QuestionType: int = Form(0), KnowledgeID: int = Form(0), Description: str = Form('')) -> Result:
    Token = Token.strip()
    QuestionTitle = QuestionTitle.strip()
    Description = Description.strip()
    return questionLogic.NewQuestion(request.client.host, Token, QuestionTitle, QuestionType, KnowledgeID, Description)
