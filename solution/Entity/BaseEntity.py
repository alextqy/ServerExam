from Service.Cache import *
from Service.Common import *
from Service.Database import *
from Service.File import *
from Service.Lang import *
from Service.UDPTool import *

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, INTEGER, DECIMAL, String
from sqlalchemy.orm import relationship
# from sqlalchemy.exc import *

SQLALCHEMY_DATABASE_URL = 'sqlite:///./DaoRoom.db'
DBEngine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
DBsession = sessionmaker(autocommit=False, autoflush=False, bind=DBEngine)
BaseORM = declarative_base()


class BaseEntity:
    ID: int = Column(INTEGER, primary_key=True, index=True, comment='ID')
    CreateTime: int = Column(INTEGER(10), comment='创建时间', default=int(time()))

    def __init__(self):
        super().__init__()