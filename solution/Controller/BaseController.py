from Service.Cache import *
from Service.Common import *
from Service.Database import *
from Service.File import *
from Service.Lang import *
from Service.UDPTool import *

from fastapi import FastAPI, APIRouter, File, UploadFile, Request, Form
from Logic.ExamineeLogic import ExamineeLogic

examineelogic = ExamineeLogic()