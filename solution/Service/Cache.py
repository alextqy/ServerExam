# -*- coding:utf-8 -*-
from Service.BaseService import *


class Cache(BaseService):

    def __init__(self, Path='', jsonFile='cache.json'):
        self.jsonFile = Path + jsonFile
        self.configData = OrderedDict()
        if Path == '':
            self.configData = {'Debug': False, 'URL': '', 'SwitchHttps': False, 'Account': '', 'Title': 'BIT EXAM', 'Lang': '', 'Token': '', 'TokenType': '', 'Sync': False, 'ServerPort': 6002, 'SynchronizationCycle': 3}

        selectFile = isfile(self.jsonFile)
        if selectFile == False:
            with open(self.jsonFile, 'w', encoding='utf-8') as f:
                dump(self.configData, f, indent=2, sort_keys=True, ensure_ascii=False)  # 写为多行

    def Select(self):
        try:
            with open(self.jsonFile, encoding='utf-8') as f:
                data = load(f)
            return data
        except OSError as e:
            return

    def Get(self, k):
        with open(self.jsonFile, encoding='utf-8') as f:
            data = load(f)

        if k in data.keys():
            return data[k]
        else:
            return None

    def Set(self, k, v):
        self.configData = self.Select()
        if k in self.configData:
            self.configData[k] = v
        else:
            self.configData = {**self.configData, **{k: v}}  # 数据合并
        try:
            with open(self.jsonFile, 'w', encoding='utf-8') as f:
                dump(self.configData, f, indent=2, sort_keys=True, ensure_ascii=False)  # 写入多行
        except OSError as e:
            return

    def Delete(self, k):
        self.configData = self.Select()
        if k in self.configData:
            self.configData.pop(k)
        else:
            return
        try:
            with open(self.jsonFile, 'w', encoding='utf-8') as f:
                dump(self.configData, f, indent=2, sort_keys=True, ensure_ascii=False)  # 写入多行
        except OSError as e:
            return

    def Append(self, k, v):
        data = self.Get(k)
        if type(v) == list:
            data.extend(v)
        elif type(v) == str:
            data = data + 'v'
        else:
            data = v
        self.configData[k] = data
