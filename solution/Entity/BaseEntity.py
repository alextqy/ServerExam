from Service.Cache import *
from Service.Common import *
from Service.Database import *
from Service.FileHelper import *
from Service.Lang import *
from Service.UDPTool import *

SQLALCHEMY_DATABASE_URL = 'sqlite:///./DaoRoom.db'
DBEngine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
DBsession = sessionmaker(autocommit=False, autoflush=False, bind=DBEngine)
BaseORM = declarative_base()


class BaseEntity:
    ID: int = Column(INTEGER, primary_key=True, index=True, comment='ID')
    CreateTime: int = Column(INTEGER, comment='创建时间', default=int(time()))

    def __init__(self):
        super().__init__()