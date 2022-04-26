# -*- coding:utf-8 -*-
from Service.BaseService import *


class Result:
    Status: bool
    Memo: str
    Code: int
    Data: None

    def __init__(self) -> None:
        super().__init__()
        self.Status = False
        self.Memo = ''
        self.Code = 200
        self.Data = None


class ResultList:
    Status: bool
    Memo: str
    Code: int
    Data: None
    Page: int
    PageSize: int
    TotalPage: int

    def __init__(self) -> None:
        super().__init__()
        self.Status = False
        self.Memo = ''
        self.Code = 200
        self.Data = None
        self.Page = 0
        self.PageSize = 0
        self.TotalPage = 0


class Common(BaseService):

    def __init__(self):
        super().__init__()

    # 判断操作系统类型
    def OSType(self):
        osType = system()
        if osType == "Windows":
            return osType
        elif osType == "Linux":
            return osType
        elif osType == "Darwin":
            return "MacOS"
        else:
            return "Other"

    # 获取CPU序列号
    def CPUID(self):
        osType = self.OSType()
        if osType == "Windows":
            from wmi import WMI
            _wmi = WMI()
            for _, cpu in enumerate(_wmi.Win32_Processor()):
                cpuInfo = cpu
            return cpuInfo.ProcessorId.strip()
        elif osType == "Linux":
            cpuInfo = os.system("sudo dmidecode -t 4 | grep ID")
            return cpuInfo.decode("utf8").strip().replace("ID:", "").replace(" ", "")
        else:
            return ""

    # 获取主板序列号
    def MotherboardID(self):
        osType = self.OSType()
        if osType == "Windows":
            from wmi import WMI
            _wmi = WMI()
            boardInfo = _wmi.Win32_BaseBoard()[0].SerialNumber
            return boardInfo.strip().replace(" ", "")
        elif osType == "Linux":
            boardInfo = os.popen("sudo dmidecode -t 1 | grep Serial").read()
            return boardInfo.strip().replace("Serial Number:", "").replace(" ", "")
        else:
            return ""

    # 字符串过滤 只匹配大小写字母和数字的组合
    def MatchAll(self, Param=""):
        if Param == "":
            return False
        elif search("^[a-zA-Z0-9_]+$", Param) == None:
            return False
        else:
            return True

    # 字符串过滤 只匹配小写字母
    def MatchStr(self, Param=""):
        if Param == "":
            return False
        elif search("^[a-z_]+$", Param) == None:
            return False
        else:
            return True

    # 字符串过滤 只匹配数字
    def MatchNum(self, Param=""):
        if Param == "":
            return False
        elif search("^[0-9]+$", Param) == None:
            return False
        else:
            return True

    # 大小写字母 中文 数字 下划线 点
    def MatchSafe(self, Param=""):
        if Param == "":
            return False
        elif search("^[\u4E00-\u9FA5A-Za-z0-9_.]+$", Param) == None:
            return False
        else:
            return True

    # 年
    def NowYear(self):
        return datetime.datetime.now().year

    # 月
    def NowMonth(self):
        return datetime.datetime.now().month

    # 日
    def NowDay(self):
        return datetime.datetime.now().day

    # 时间戳转换成时间(接收10位str时间戳)
    def TimeToStr(self, TimeNum):
        timeData = localtime(int(str(TimeNum)[:10]))
        return strftime("%Y-%m-%d %H:%M:%S", timeData)

    # 时间转换成时间戳
    def StrToTime(self, TimeStr):
        timeFormat = strptime(TimeStr, "%Y-%m-%d %H:%M:%S")
        return int(mktime(timeFormat))

    # 当前时间戳
    def Time(self):
        return int(time())

    # 当前时间戳(毫秒)
    def TimeMS(self):
        return int(round(time() * 1000))

    # 获取当天的年月日
    def TodayStr(self):
        timeData = localtime(self.Time())
        return strftime("%Y-%m-%d 00:00:00", timeData)

    # 过去的时间
    def TimePast(self, Day=0):
        return self.StrToTime(self.TodayStr()) - (Day * (60 * 60 * 24))

    # 未来的时间
    def TimeFuture(self, Day=0):
        return self.StrToTime(self.TodayStr()) + (Day * (60 * 60 * 24))

    # 指定时间的过去天数
    def TheTimePast(self, Time, Day=0):
        return Time - (Day * (60 * 60 * 24))

    # 指定时间的未来天数
    def TheTimeFuture(self, Time, Day=0):
        return Time + (Day * (60 * 60 * 24))

    # 按指定字符切割字符串为数组
    def Explode(self, Separator, StringParam):
        return StringParam.split(Separator)

    # 按指定字符组合数组为字符串
    def Implode(self, Separator, array):
        return Separator.join(array)

    # 获取本机IP
    def LocalIP(self):
        try:
            s = socket(AF_INET, SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    # 图片转Base64
    def IMGToBase64(self, FilePath):
        with open(FilePath, 'rb') as f:  # 以二进制读取图片
            FileEncode = b64encode(f.read())  # 得到 byte 编码的数据
            FileEncodeStr = str(FileEncode, "utf-8")  # 重新编码数据
        return FileEncodeStr

    # 发送邮件
    def SendMail(self, Content=""):
        if Content == "":
            return False

        # MailHost = ""  # SMTP服务器
        # MailUser = ""  # 用户名
        # MailPass = ""  # 密码(这里的密码不是登录邮箱密码，而是授权码)
        # Sender = ""  # 发件人邮箱
        # Receivers = [""]  # 接收人邮箱
        # Title = 'BitBox Suggestions & Opinion'  # 邮件主题
        # Message = MIMEText(Content, "plain", "utf-8")  # 内容, 格式, 编码
        # Message['From'] = "{}".format(Sender)
        # Message['To'] = ",".join(Receivers)
        # Message['Subject'] = Title
        # try:
        #     # smtpObj = smtplib.SMTP(MailHost, 465)  # 不启用SSL发信, 端口一般是465
        #     smtpObj = smtplib.SMTP_SSL(MailHost, 465)  # 启用SSL发信, 端口一般是465
        #     smtpObj.login(MailUser, MailPass)  # 登录验证
        #     smtpObj.sendmail(Sender, Receivers, Message.as_string())  # 发送
        #     return True
        # except smtplib.SMTPException as e:
        #     return False

        mailFrom = 'alextqy@qq.com'  # 发送方邮箱
        smtpObj = MIMEMultipart()
        smtpObj.attach(MIMEText(Content, 'plain', 'utf-8'))
        smtpObj['Subject'] = "BitBox Suggestions & Opinion"
        smtpObj['From'] = mailFrom
        email = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 通过SSL方式发送，服务器地址和端口
        email.login(mailFrom, "rkswvfmitwzlbggd")  # 登录邮箱
        try:
            email.sendmail(mailFrom, "285150667@qq.com", smtpObj.as_string())  # 开始发送
            return True
        except smtplib.SMTPException as e:
            return False

    # str to bytes
    def StringToBytes(self, Param):
        return bytes(Param, encoding="utf8")

    # bytes to str
    def BytesToString(self, Param):
        return str(Param, encoding="utf-8")

    # bytes to Base64
    def BytesToBase64(self, Param):
        return b64encode(Param)

    # Base64 to bytes
    def Base64ToBytes(self, Param):
        return b64decode(Param)

    # 字符串MD5
    def StrMD5(self, Param):
        return md5(Param.encode('utf-8')).hexdigest()
