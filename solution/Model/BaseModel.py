from Service.Cache import *
from Service.Common import *
from Service.Database import *
from Service.File import *
from Service.Lang import *
from Service.UDPTool import *

from Entity.BaseEntity import *
# from sqlalchemy.exc import *
from Entity.ExamineeEntity import ExamineeEntity
from Entity.ExamineeTokenEntity import ExamineeTokenEntity



class BaseModel:
    _cache: Cache()
    _common: Common()
    _file: File()
    _lang: Lang()
    _udp: UDPTool()

    def __init__(self):
        super().__init__()
        self._cache = Cache()
        self._common = Common()
        self._file = File()
        self._lang = Lang()
        self._udp = UDPTool()