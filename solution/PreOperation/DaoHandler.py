# -*- coding:utf-8 -*-
from Logic.BaseLogic import *


class DaoHandler(BaseLogic):

    def __init__(self):
        super().__init__()

    def AddFields(self):
        _common = Common()
        ConfigObj: dict = _common.ReadJsonFile(path[0] + '/config.json')
        SQLALCHEMY_DATABASE_URI: str = 'mysql+pymysql://root:' + ConfigObj['DaoPWD'] + '@' + ConfigObj['DaoURL'] + '/server-exam'
        DBEngine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
        try:
            with DBEngine.connect() as con:
                sql = "ALTER TABLE `ExamInfoHistory` ADD COLUMN `ExamType` tinyint(1) unsigned zerofill DEFAULT NULL COMMENT '考试类型 1正式考试 2练习';"
                tables = con.execute(sql).fetchall()
        except Exception as e:
            print('Pre-Operation finish')