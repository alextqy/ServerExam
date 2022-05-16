from Controller.BaseController import *

QuestionSolutionRouter = APIRouter()
QuestionSolutionPrefix = ''


# 新建试题答案
@QuestionSolutionRouter.post('/New/Question/Solution')
async def NewQuestionSolution(
        request: Request,
        Token: str = Form(''),
        QuestionID: int = Form(''),
        Option: str = Form(''),
        CorrectAnswer: int = Form(0),
        CorrectItem: str = Form(''),
        ScoreRatio: float = Form(1),
        Position: int = Form(1),
) -> Result:
    return questionSolutionLogic.NewQuestionSolution(request.client.host, Token.strip(), QuestionID, Option.strip(), CorrectAnswer, CorrectItem, ScoreRatio, Position)
