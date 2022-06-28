from Entity.BaseEntity import *


# 试卷
class PaperEntity(BaseEntity, BaseORM):
    __tablename__ = 'Paper'

    PaperName: str = Column(String(128), comment='试卷名称', default='none')
    PaperCode: str = Column(String(128), index=True, comment='试卷编码', default='none')
    SubjectID: int = Column(INTEGER, comment='科目ID', default=0)
    TotalScore: float = Column(DECIMAL(10, 2), comment='总分', default=0.00)
    PassLine: float = Column(DECIMAL(10, 2), comment='及格分数', default=0.00)
    ExamDuration: int = Column(INTEGER, comment='考试时长', default=0)
    PaperState: int = Column(INTEGER, comment='试卷状态 1正常 2禁用', default=0)
    UpdateTime: int = Column(INTEGER, comment='更新时间', default=int(time()))

    def __init__(self):
        super().__init__()