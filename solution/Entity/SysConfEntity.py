from Entity.BaseEntity import *


# 系统配置
class SysConfEntity(BaseEntity):
    __tablename__ = 'SysConf'

    Type = Column(INTEGER, comment='配置类型')
    Key = Column(String(128), comment='配置KEY')
    Value = Column(String(128), comment='配置Value')
    Describe = Column(String(128), comment='配置描述')