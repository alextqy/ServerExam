# -*- coding:utf-8 -*-
import os
import smtplib
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
from math import *
from shutil import *
from subprocess import *
from io import *
from base64 import *
import base64
from requests import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
import zipfile
import datetime
import math
import random
import string
import json
from random import sample, choice
from threading import *

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, INTEGER, DECIMAL, String
from sqlalchemy.orm import relationship
from sqlalchemy import asc, desc, and_, or_
# from sqlalchemy.exc import *

import xlrd

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import FastAPI, APIRouter, File, UploadFile, Request, Form, Body
from fastapi import Cookie
from starlette.requests import Request


class BaseService():

    def __init__(self):
        super().__init__()
