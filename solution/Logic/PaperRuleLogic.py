from Logic.BaseLogic import *


class PaperRuleLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewPaperRule(self, Token: str, HeadlineID: int, QuestionType: int, QuestionNum: int, SingleScore: float, PaperID: int, PaperRuleState: int) -> Result:
        pass