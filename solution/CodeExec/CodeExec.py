# -*- coding:utf-8 -*-
import os
from socket import *
from os import *
from os.path import *
from functools import *
from collections import *
from platform import *
from re import *
from time import *
from json import *
from stat import *
from hashlib import *
from sys import *
from base64 import *
from math import *
from shutil import *
from io import *
from base64 import *
import json
from fastapi import FastAPI, File
from fastapi import APIRouter
from fastapi import FastAPI, Form
from fastapi import Cookie
from starlette.requests import Request
import base64

# uvicorn main:app --host=0.0.0.0 --port=8181 --reload


class Result:

    def __init__(self):
        super().__init__()
        self.State = False
        self.Memo = "未知错误"
        self.Data = ""
        self.ID = 0


def OSType():
    osType = system()
    if osType == "Windows":
        return osType
    elif osType == "Linux":
        return osType
    elif osType == "Darwin":
        return "MacOS"
    else:
        return "Other"


def CLI(Code=""):
    return os.popen(Code).read()


app = FastAPI()
Router = APIRouter()


@Router.get("/Clean/Temp/File")
async def CleanTempFile(request: Request):
    CodeDir = getcwd() + "/Code/"  # 代码执行文件夹
    try:
        rmtree(CodeDir, ignore_errors=False, onerror=None)
        mkdir(CodeDir)
        return "ok"
    except:
        return "error"


@Router.post("/Code/Exec")
async def CheckExamInfo(request: Request, Key: str = Form(...), Language: str = Form(...), Version: str = Form(...), CodeStr: str = Form(...), ExamInfoID: int = Form(...)):
    ServerKey = "TXNGG3KidItKrCGf5wXT53eZTYCOynOAIjbKJPdy"
    CodeFilePath = getcwd() + "/CodeFile/"  # 模板文件夹
    CodeDir = getcwd() + "/Code/"  # 代码执行文件夹
    result = Result()

    CheckCliInfo = ""  # 正确答案比对参数
    # print("原始数据:")
    # print(CodeStr)
    # print(".....")
    try:
        CodeStr = base64.b64decode(CodeStr).decode("utf-8")
    # except Exception as e:
    #     print(e)
    except OSError as err:
        # print("OS error: {0}".format(err))
        result.Memo = "代码解析失败"
        result.Data = ""
        return result
    # print("解码数据:")
    # print(CodeStr)
    # print(".....")

    if Key != ServerKey:
        result.Memo = "密匙有误"
    elif Language == "":
        result.Memo = "实训语言有误"
    elif Version == "":
        result.Memo = "实训语言版本有误"
    elif CodeStr == "":
        result.Memo = "执行代码有误"
    elif ExamInfoID <= 0:
        result.Memo = "报名ID有误"
    else:
        Language = Language.lower()

        if Language == "php":
            TempFile = "php.php"
        elif Language == "javascript":
            TempFile = "javascript.js"
        elif Language == "python":
            TempFile = "python.py"
        elif Language == "java":
            TempFile = "java.java"
        elif Language == "c":
            TempFile = "c.c"
        else:
            TempFile = ""

        if Language == "php":
            LangSuffix = ".php"
        elif Language == "javascript":
            LangSuffix = ".js"
        elif Language == "python":
            LangSuffix = ".py"
        elif Language == "java":
            LangSuffix = ".java"
        elif Language == "c":
            LangSuffix = ".c"
        else:
            LangSuffix = ""

        if Language == "php":
            DockerRun = "docker run " + " --rm -it -v " + CodeDir + ":/home/code -w /home/code php:" + Version + " php " + str(ExamInfoID) + ".php",
        elif Language == "javascript":
            DockerRun = "docker run " + " --rm -it -v " + CodeDir + ":/home/code -w /home/code node node " + str(ExamInfoID) + ".js",
        elif Language == "python":
            DockerRun = "docker run " + " --rm -it -v " + CodeDir + ":/home/code -w /home/code python:" + Version + " python " + str(ExamInfoID) + ".py",
        elif Language == "java":
            DockerRun = "docker run " + " --rm -it -v " + CodeDir + ":/home/code -w /home/code",
        elif Language == "c":
            DockerRun = "docker run " + " --rm -it -v " + CodeDir + ":/home/code -w /home/code",
        else:
            DockerRun = ""
        try:
            if LangSuffix != "" and DockerRun != "":
                FilePath = CodeFilePath + TempFile
                f = open(FilePath, "r")
                FileContent = f.read()
                f.close()

                if FileContent != "":
                    FileContent = FileContent.replace("[CODE]", CodeStr)
                    if Language == "java":
                        FileContent = FileContent.replace("[NAME]", "Test" + str(ExamInfoID))

                CodeFile = ""  # 代码运行文件
                if Language == "java":
                    CodeFile = CodeDir + "Test" + str(ExamInfoID) + LangSuffix
                else:
                    CodeFile = CodeDir + str(ExamInfoID) + LangSuffix

                try:
                    file = open(CodeFile, "w")
                    file.close()
                except OSError as e:
                    # print(e)
                    # print("创建代码运行文件失败")
                    result.Memo = "创建代码运行文件失败"
                    result.Data = ""
                    return result

                try:
                    File = open(CodeFile, "w")
                    File.write(FileContent)
                    File.close()
                except OSError as e:
                    # print(e)
                    # print("写入代码运行文件失败")
                    result.Memo = "写入代码运行文件失败"
                    result.Data = ""
                    remove(CodeFile)
                    return result

                if Language == "java":
                    CLI(DockerRun[0] + " openjdk:" + Version + " javac Test" + str(ExamInfoID) + ".java")
                if Language == "c":
                    CLI("gcc " + CodeDir + str(ExamInfoID) + ".c -o " + CodeDir + str(ExamInfoID))
                # print("执行语句:")
                # print(DockerRun[0])
                # print("=====================")
                cliinfo = ""
                try:
                    if Language == "java":
                        cliinfo = json.loads(CLI(DockerRun[0] + " openjdk:" + Version + " java Test" + str(ExamInfoID)))
                    elif Language == "c":
                        print(CLI(DockerRun[0] + " gcc /home/code/" + str(ExamInfoID)))
                        # cliinfo = json.loads(CLI(DockerRun[0] + " gcc /home/code/" + str(ExamInfoID)))
                    else:
                        cliinfo = json.loads(CLI(DockerRun[0]))

                    CheckCliInfo = cliinfo["Result"]
                    # print("输出结果字符串 " + CheckCliInfo)
                    # print("==========")

                    # 是否有语法错误
                    if "error" in CheckCliInfo:
                        result.Data = "null"
                    elif "err" in CheckCliInfo:
                        result.Data = "null"
                    else:
                        result.Data = CheckCliInfo

                    result.Memo = "Success"
                    result.State = True
                    remove(CodeFile)
                except OSError as e:
                    # print("执行结果异常")
                    # print(e)
                    # print("===========")
                    result.Memo = "代码执行失败"
                    result.Data = ""
                    remove(CodeFile)
        except OSError as e:
            result.Memo = "代码执行失败"
            result.Data = ""

    # 删除执行完成的文件(重要)
    if Language == "java":
        remove(CodeDir + "Test" + str(ExamInfoID) + ".class")
        # remove(CodeDir + "Test" + str(ExamInfoID) + ".java")

    return result


app.include_router(Router)
