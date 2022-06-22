from Controller.BaseController import *

ExerciseRouter = APIRouter()
ExercisePrefix = ''


@ExerciseRouter.post('/Sign/In/Exercise')
async def SignInExercise(
    request: Request,
    ExamineeNo: str,
) -> Result:
    return exerciseLogic.SignInExercise(ExamineeNo)


@ExerciseRouter.post('/New/Exercise')
async def NewExercise(
        request: Request,
        Token: str = Form(''),
) -> Result:
    return exerciseLogic.NewExercise(Token)