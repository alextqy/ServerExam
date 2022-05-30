from Controller.BaseController import *

PaperRuleRouter = APIRouter()
PaperRulePrefix = ''


# 新建试卷规则
@PaperRuleRouter.post('/New/Paper/Rule')
async def NewPaperRule(
        request: Request,
        Token: str = Form(''),
        HeadlineID: int = Form(0),
        QuestionType: int = Form(0),
        KnowledgeID: int = Form(0),
        QuestionNum: int = Form(0),
        SingleScore: float = Form(0),
        PaperID: int = Form(0),
) -> Result:
    return paperRuleLogic.NewPaperRule(request.client.host, Token.strip(), HeadlineID, QuestionType, KnowledgeID, QuestionNum, SingleScore, PaperID)
