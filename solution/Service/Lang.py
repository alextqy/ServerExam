# -*- coding:utf-8 -*-
from Service.BaseService import *
from Service.Cache import *


class Lang(BaseService):

    def __init__(self, Type: str = ''):
        super().__init__()
        self.Type = Type

        # 英文
        if self.Type == "en":
            self.Account = "Account"
            self.Name = "Name"
            self.PWD = "Password"
            self.IP = "IP"

        # 中文简体
        elif self.Type == "zh-cn":
            self.Account = "账号"
            self.Name = "姓名"
            self.PWD = "密码"
            self.IP = "IP"

        # 中文繁体
        elif self.Type == "zh-tw":
            self.Account = "賬號"
            self.Name = "姓名"
            self.PWD = "密碼"
            self.IP = "IP"

        # 默认
        else:
            self.Account = ""
            self.Name = ""
            self.PWD = ""
            self.IP = ""