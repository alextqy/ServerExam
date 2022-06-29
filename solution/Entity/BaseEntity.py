# -*- coding:utf-8 -*-
from Service.Cache import *
from Service.Common import *
from Service.Database import *
from Service.FileHelper import *
from Service.Lang import *
from Service.UDPTool import *

_common = Common()
ConfigObj: dict = _common.ReadJsonFile(path[0] + '/config.json')

# SQLALCHEMY_DATABASE_URI = 'sqlite:///./DaoRoom.db'
# DBEngine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={'check_same_thread': False})

SQLALCHEMY_DATABASE_URI: str = 'mysql+pymysql://root:' + ConfigObj['DaoPWD'] + '@' + ConfigObj['DaoURL'] + '/server-exam'
DBEngine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
# mysql内置压测工具 范例 J4125 4G
# sudo mysqlslap -hlocalhost -uroot -p123456 -P3306 --concurrency=3000 --iterations=1 --auto-generate-sql --auto-generate-sql-load-type=mixed --auto-generate-sql-add-autoincrement --engine=innodb --number-of-queries=3000

DBsession = sessionmaker(autocommit=False, autoflush=False, bind=DBEngine)
BaseORM = declarative_base()


class BaseEntity:
    ID: int = Column(INTEGER, primary_key=True, index=True, comment='ID')
    CreateTime: int = Column(INTEGER, comment='创建时间', default=int(time()))

    def __init__(self):
        super().__init__()