from Entity.BaseEntity import *


# 大标题
class HeadlineEntity(BaseEntity, BaseORM):
    __tablename__ = 'Headline'

    Content: str = Column(String(65535), comment='内容')
    ContentCode: str = Column(String(128), comment='内容编码')
    UpdateTime: int = Column(INTEGER, comment='更新时间', default=int(time()))

    def __init__(self):
        super().__init__()

    def SetContent(self, Value: str):
        if isinstance(Value, str):
            self.Content = Value.strip()

    def SetContentCode(self, Value: str):
        if isinstance(Value, str):
            self.ContentCode = Value.strip()

    def SetUpdateTime(self, Value: int):
        if isinstance(Value, int):
            self.UpdateTime = Value