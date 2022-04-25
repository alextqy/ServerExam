from sqlalchemy import Column, INTEGER, DECIMAL, String
from sqlalchemy.orm import relationship


class BaseEntity:
    ID = Column(INTEGER, primary_key=True, index=True, comment='ID')
    CreateTime = Column(INTEGER, comment='创建时间')