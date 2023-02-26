# -*- coding:utf-8 -*-
from Service.Cache import *
from Service.Common import *
from Service.Database import *
from Service.FileHelper import *
from Service.Lang import *
from Service.UDPTool import *
from sqlalchemy.orm import Mapped

_common = Common()
ConfigObj: dict = _common.ReadJsonFile(path[0] + '/config.json')

# SQLALCHEMY_DATABASE_URI = 'sqlite:///./DaoRoom.db'
# DBEngine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={'check_same_thread': False})

SQLALCHEMY_DATABASE_URI: str = 'mysql+pymysql://root:' + ConfigObj['DaoPWD'] + '@' + ConfigObj['DaoURL'] + '/server-exam'
DBEngine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    # pool_size=20,
    # max_overflow=0,
    # pool_pre_ping=True,
    echo=False,
    pool_size=0,
    pool_timeout=1,
    pool_recycle=30,
    max_overflow=-1,
    pool_pre_ping=True,
    isolation_level='READ UNCOMMITTED',
)
# mysql内置压测工具 范例 J4125 4G
# sudo mysqlslap -hlocalhost -uroot -p123456 -P3306 --concurrency=3000 --iterations=1 --auto-generate-sql --auto-generate-sql-load-type=mixed --auto-generate-sql-add-autoincrement --engine=innodb --number-of-queries=3000

DBsession = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=DBEngine,
    expire_on_commit=False,
    __allow_unmapped__=True,
)
BaseORM = declarative_base()


class BaseEntity:
    ID: Mapped[int] = Column(INTEGER, primary_key=True, index=True, comment='ID')
    CreateTime: Mapped[int] = Column(INTEGER, comment='创建时间', default=0)

    def __init__(self):
        super().__init__()