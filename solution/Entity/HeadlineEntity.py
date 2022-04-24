from Entity.BaseEntity import *


# 大标题
class HeadlineEntity(BaseEntity):
    __tablename__ = 'Headline'

    Content = Column(String(65535), comment='内容')
    ContentCode = Column(String(128), comment='内容编码')
    UpdateTime = Column(INTEGER, comment='更新时间')
