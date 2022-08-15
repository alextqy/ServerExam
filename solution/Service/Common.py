# -*- coding:utf-8 -*-
from Service.BaseService import *


class Result:
    State: bool
    Memo: str
    Code: int
    Data: None

    def __init__(self) -> None:
        super().__init__()
        self.State = False
        self.Memo = ''
        self.Code = 200
        self.Data = None


class ResultList:
    State: bool
    Memo: str
    Code: int
    Page: int
    PageSize: int
    TotalPage: int
    Data: None

    def __init__(self) -> None:
        super().__init__()
        self.State = False
        self.Memo = ''
        self.Code = 200
        self.Page = 0
        self.PageSize = 0
        self.TotalPage = 0
        self.Data = None


class Common(BaseService):

    def __init__(self):
        super().__init__()

    # 判断操作系统类型
    def OSType(self) -> str:
        osType = system()
        if osType == 'Windows':
            return osType
        elif osType == 'Linux':
            return osType
        elif osType == 'Darwin':
            return 'MacOS'
        else:
            return 'Other'

    # 获取CPU序列号
    def CPUID(self) -> str:
        osType = self.OSType()
        if osType == 'Windows':
            from wmi import WMI
            _wmi = WMI()
            for _, cpu in enumerate(_wmi.Win32_Processor()):
                cpuInfo = cpu
            return cpuInfo.ProcessorId.strip()
        elif osType == 'Linux':
            cpuInfo = os.system('sudo dmidecode -t 4 | grep ID')
            return cpuInfo.decode('utf8').strip().replace('ID:', '').replace(' ', '')
        else:
            return ''

    # 获取主板序列号
    def MotherboardID(self) -> str:
        osType = self.OSType()
        if osType == 'Windows':
            from wmi import WMI
            _wmi = WMI()
            boardInfo = _wmi.Win32_BaseBoard()[0].SerialNumber
            return boardInfo.strip().replace(' ', '')
        elif osType == 'Linux':
            boardInfo = os.popen('sudo dmidecode -t 1 | grep Serial').read()
            return boardInfo.strip().replace('Serial Number:', '').replace(' ', '')
        else:
            return ''

    # 字符串过滤 只匹配大小写字母和数字的组合
    def MatchAll(self, Param: str) -> bool:
        if Param == '':
            return False
        elif search('^[a-zA-Z0-9_]+$', Param) == None:
            return False
        else:
            return True

    # 字符串过滤 只匹配小写字母
    def MatchStr(self, Param: str) -> bool:
        if Param == '':
            return False
        elif search('^[a-z_]+$', Param) == None:
            return False
        else:
            return True

    # 字符串过滤 只匹配数字
    def MatchNum(self, Param: str) -> bool:
        if Param == '':
            return False
        elif search('^[0-9]+$', Param) == None:
            return False
        else:
            return True

    # 大小写字母 中文 数字 下划线 点
    def MatchSafe(self, Param: str) -> bool:
        if Param == '':
            return False
        elif search('^[\u4E00-\u9FA5A-Za-z0-9_.]+$', Param) == None:
            return False
        else:
            return True

    # 年
    def NowYear(self) -> int:
        return datetime.datetime.now().year

    # 月
    def NowMonth(self) -> int:
        return datetime.datetime.now().month

    # 日
    def NowDay(self) -> int:
        return datetime.datetime.now().day

    # 时间戳转换成时间(接收10位str时间戳)
    def TimeToStr(self, TimeNum: int) -> str:
        timeData = localtime(int(str(TimeNum)[:10]))
        return strftime('%Y-%m-%d %H:%M:%S', timeData)

    # 时间转换成时间戳
    def StrToTime(self, TimeStr: str) -> int:
        timeFormat = strptime(TimeStr, '%Y-%m-%d %H:%M:%S')
        return int(mktime(timeFormat))

    # 当前时间戳
    def Time(self) -> int:
        return int(time())

    # 当前时间戳(毫秒)
    def TimeMS(self) -> int:
        return int(round(time() * 1000))

    # 获取当天的年月日
    def TodayStr(self) -> str:
        timeData = localtime(self.Time())
        return strftime('%Y-%m-%d 00:00:00', timeData)

    # 过去的时间
    def TimePast(self, Day: int) -> int:
        return self.StrToTime(self.TodayStr()) - (Day * (60 * 60 * 24))

    # 未来的时间
    def TimeFuture(self, Day: int) -> int:
        return self.StrToTime(self.TodayStr()) + (Day * (60 * 60 * 24))

    # 指定时间的过去天数
    def TheTimePast(self, Time: int, Day: int) -> int:
        return Time - (Day * (60 * 60 * 24))

    # 指定时间的未来天数
    def TheTimeFuture(self, Time: int, Day: int) -> int:
        return Time + (Day * (60 * 60 * 24))

    # 按指定字符切割字符串为数组
    def Explode(self, Separator: str, StringParam: str) -> list:
        return StringParam.split(Separator)

    # 按指定字符组合数组为字符串
    def Implode(self, Separator: str, array) -> str:
        return Separator.join(array)

    # 指定字符在字符串中出现的次数
    def CountStr(self, ParamStr: str, TargetStr: str) -> int:
        return ParamStr.count(TargetStr)

    # 获取本机IP
    # def LocalIP(self) -> str:
    #     try:
    #         s = socket(AF_INET, SOCK_DGRAM)
    #         s.connect(('8.8.8.8', 80))
    #         ip = s.getsockname()[0]
    #     finally:
    #         s.close()
    #     return ip

    def LocalIP(self) -> str:
        import requests
        CallbackInfo = requests.get('https://www.baidu.com', stream=True)
        return CallbackInfo.raw._connection.sock.getsockname()[0]

    # 图片转Base64
    def IMGToBase64(self, FilePath: str) -> str:
        with open(FilePath, 'rb') as f:  # 以二进制读取图片
            FileEncode = b64encode(f.read())  # 得到 byte 编码的数据
            FileEncodeStr = str(FileEncode, 'utf-8')  # 重新编码数据
        return FileEncodeStr

    # 发送邮件
    def SendMail(self, Content: str) -> bool:
        if Content == '':
            return False

        # MailHost = ''  # SMTP服务器
        # MailUser = ''  # 用户名
        # MailPass = ''  # 密码(这里的密码不是登录邮箱密码，而是授权码)
        # Sender = ''  # 发件人邮箱
        # Receivers = ['']  # 接收人邮箱
        # Title = 'BIT EXAM Suggestions & Opinion'  # 邮件主题
        # Message = MIMEText(Content, 'plain', 'utf-8')  # 内容, 格式, 编码
        # Message['From'] = '{}'.format(Sender)
        # Message['To'] = ','.join(Receivers)
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
        smtpObj['Subject'] = 'BIT EXAM Suggestions & Opinion'
        smtpObj['From'] = mailFrom
        email = smtplib.SMTP_SSL('smtp.qq.com', 465)  # 通过SSL方式发送，服务器地址和端口
        email.login(mailFrom, 'rkswvfmitwzlbggd')  # 登录邮箱
        try:
            email.sendmail(mailFrom, '285150667@qq.com', smtpObj.as_string())  # 开始发送
            return True
        except smtplib.SMTPException as e:
            return False

    # str to bytes
    def StringToBytes(self, Param: str) -> bytes:
        return bytes(Param, encoding='utf8')

    # bytes to str
    def BytesToString(self, Param: bytes) -> str:
        return str(Param, encoding='utf-8')

    # bytes to Base64
    def BytesToBase64(self, Param: bytes) -> bytes:
        return b64encode(Param)

    # Base64 to bytes
    def Base64ToBytes(self, Param: bytes) -> bytes:
        return b64decode(Param)

    # a-zA-Z1-9随机数
    def RandomStr(self, n=10) -> str:
        return ''.join(random.sample(string.ascii_letters + string.digits, n))

    # 字符串MD5
    def StrMD5(self, Param: str) -> str:
        return md5(Param.encode('utf-8')).hexdigest()

    # 生成密码
    def UserPWD(self, Param: str) -> str:
        return self.StrMD5(self.StrMD5(Param) + Param)

    # 生成Token
    def GenerateToken(self) -> str:
        return self.StrMD5(self.RandomStr())

    # 解析json文件
    def ReadJsonFile(self, FilePath: str) -> dict:
        f = open(FilePath, 'r')
        Data = f.read()
        f.close()
        return json.loads(Data)

    # 随机抽取数组中一个元素
    def RandomDrawChoice(self, Array: list) -> any:
        return choice(Array)

    # 随机抽取数组中多个不重复元素
    def RandomDrawSample(self, Array: list, Quantity: int) -> list:
        return sample(Array, Quantity)

    # 执行Linux命令行
    def CLI(self, Code=''):
        return os.popen(Code).read()

    # MIME类型查询
    def MIME(self, TypeInfo: str) -> str:
        if TypeInfo == '':
            TypeInfo = ''
        else:
            TypeInfo = TypeInfo.lower()
            if TypeInfo == 'audio/aac':
                TypeInfo = '.acc'
            elif TypeInfo == 'application/x-abiword':
                TypeInfo = '.abw'
            elif TypeInfo == 'application/x-freearc':
                TypeInfo = '.arc'
            elif TypeInfo == 'video/x-msvideo':
                TypeInfo = '.avi'
            elif TypeInfo == 'application/vnd.amazon.ebook':
                TypeInfo = '.azw'
            elif TypeInfo == 'application/octet-stream':
                TypeInfo = '.bin'
            elif TypeInfo == 'image/bmp':
                TypeInfo = '.bmp'
            elif TypeInfo == 'application/x-bzip':
                TypeInfo = '.bz'
            elif TypeInfo == 'application/x-bzip2':
                TypeInfo = '.bz2'
            elif TypeInfo == 'application/x-csh':
                TypeInfo = '.csh'
            elif TypeInfo == 'text/css':
                TypeInfo = '.css'
            elif TypeInfo == 'text/csv':
                TypeInfo = '.csv'
            elif TypeInfo == 'application/msword':
                TypeInfo = '.doc'
            elif TypeInfo == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                TypeInfo = '.docx'
            elif TypeInfo == 'application/vnd.ms-fontobject':
                TypeInfo = '.eot'
            elif TypeInfo == 'application/epub+zip':
                TypeInfo = '.epub'
            elif TypeInfo == 'image/gif':
                TypeInfo = '.gif'
            elif TypeInfo == 'text/html':
                TypeInfo = '.html'
            elif TypeInfo == 'image/vnd.microsoft.icon':
                TypeInfo = '.ico'
            elif TypeInfo == 'text/calendar':
                TypeInfo = '.ics'
            elif TypeInfo == 'application/java-archive':
                TypeInfo = '.jar'
            elif TypeInfo == 'image/jpeg':
                TypeInfo = '.jpeg'
            elif TypeInfo == 'text/javascript':
                TypeInfo = '.js'
            elif TypeInfo == 'application/json':
                TypeInfo = '.json'
            elif TypeInfo == 'application/ld+json':
                TypeInfo = '.jsonld'
            elif TypeInfo == 'audio/midi':
                TypeInfo = '.mid'
            elif TypeInfo == 'audio/x-midi':
                TypeInfo = '.midi'
            elif TypeInfo == 'text/javascript':
                TypeInfo = '.mjs'
            elif TypeInfo == 'audio/mpeg':
                TypeInfo = '.mp3'
            elif TypeInfo == 'video/mpeg':
                TypeInfo = '.mpeg'
            elif TypeInfo == 'application/vnd.apple.installer+xml':
                TypeInfo = '.mpkg'
            elif TypeInfo == 'application/vnd.oasis.opendocument.presentation':
                TypeInfo = '.odp'
            elif TypeInfo == 'application/vnd.oasis.opendocument.text':
                TypeInfo = '.odt'
            elif TypeInfo == 'audio/ogg':
                TypeInfo = '.oga'
            elif TypeInfo == 'video/ogg':
                TypeInfo = '.ogv'
            elif TypeInfo == 'application/ogg':
                TypeInfo = '.ogx'
            elif TypeInfo == 'font/otf':
                TypeInfo = '.otf'
            elif TypeInfo == 'image/png':
                TypeInfo = '.png'
            elif TypeInfo == 'application/pdf':
                TypeInfo = '.pdf'
            elif TypeInfo == 'application/vnd.ms-powerpoint':
                TypeInfo = '.ppt'
            elif TypeInfo == 'application/vnd.openxmlformats-officedocument.presentationml.presentation':
                TypeInfo = '.pptx'
            elif TypeInfo == 'application/x-rar-compressed':
                TypeInfo = '.rar'
            elif TypeInfo == 'application/rtf':
                TypeInfo = '.rtf'
            elif TypeInfo == 'application/x-sh':
                TypeInfo = '.sh'
            elif TypeInfo == 'image/svg+xml':
                TypeInfo = '.svg'
            elif TypeInfo == 'application/x-shockwave-flash':
                TypeInfo = '.swf'
            elif TypeInfo == 'application/x-tar':
                TypeInfo = '.tar'
            elif TypeInfo == 'image/tiff':
                TypeInfo = '.tiff'
            elif TypeInfo == 'font/ttf':
                TypeInfo = '.ttf'
            elif TypeInfo == 'text/plain':
                TypeInfo = '.txt'
            elif TypeInfo == 'application/vnd.visio':
                TypeInfo = '.vsd'
            elif TypeInfo == 'audio/wav':
                TypeInfo = '.wav'
            elif TypeInfo == 'audio/webm':
                TypeInfo = '.weba'
            elif TypeInfo == 'video/webm':
                TypeInfo = '.webm'
            elif TypeInfo == 'image/webp':
                TypeInfo = '.webp'
            elif TypeInfo == 'font/woff':
                TypeInfo = '.woff'
            elif TypeInfo == 'font/woff2':
                TypeInfo = '.woff2'
            elif TypeInfo == 'application/xhtml+xml':
                TypeInfo = '.xhtml'
            elif TypeInfo == 'application/vnd.ms-excel':
                TypeInfo = '.xls'
            elif TypeInfo == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                TypeInfo = '.xlsx'
            elif TypeInfo == 'application/xml' or TypeInfo == 'text/xml':
                TypeInfo = '.xml'
            elif TypeInfo == 'application/vnd.mozilla.xul+xml':
                TypeInfo = '.xul'
            elif TypeInfo == 'application/zip':
                TypeInfo = '.zip'
            elif TypeInfo == 'video/3gpp' or TypeInfo == 'audio/3gpp':
                TypeInfo = '.3gp'
            elif TypeInfo == 'video/3gpp2' or TypeInfo == 'audio/3gpp2':
                TypeInfo = '.3g2'
            elif TypeInfo == 'application/x-7z-compressed':
                TypeInfo = '.7z'
            else:
                TypeInfo = ''
        return TypeInfo

    # content-type类型查询
    def ContentType(self, TypeInfo: str) -> str:
        if TypeInfo == '':
            TypeInfo = ''
        else:
            TypeInfo = TypeInfo.lower()
            if TypeInfo == '.acc':
                TypeInfo = 'audio/aac'
            elif TypeInfo == '.abw':
                TypeInfo = 'application/x-abiword'
            elif TypeInfo == '.arc':
                TypeInfo = 'application/x-freearc'
            elif TypeInfo == '.avi':
                TypeInfo = 'video/x-msvideo'
            elif TypeInfo == '.azw':
                TypeInfo = 'application/vnd.amazon.ebook'
            elif TypeInfo == '.bin':
                TypeInfo = 'application/octet-stream'
            elif TypeInfo == '.bmp':
                TypeInfo = 'image/bmp'
            elif TypeInfo == '.bz':
                TypeInfo = 'application/x-bzip'
            elif TypeInfo == '.bz2':
                TypeInfo = 'application/x-bzip2'
            elif TypeInfo == '.csh':
                TypeInfo = 'application/x-csh'
            elif TypeInfo == '.css':
                TypeInfo = 'text/css'
            elif TypeInfo == '.csv':
                TypeInfo = 'text/csv'
            elif TypeInfo == '.doc':
                TypeInfo = 'application/msword'
            elif TypeInfo == '.docx':
                TypeInfo = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            elif TypeInfo == '.eot':
                TypeInfo = 'application/vnd.ms-fontobject'
            elif TypeInfo == '.epub':
                TypeInfo = 'application/epub+zip'
            elif TypeInfo == '.gif':
                TypeInfo = 'image/gif'
            elif TypeInfo == '.html':
                TypeInfo = 'text/html'
            elif TypeInfo == '.ico':
                TypeInfo = 'image/vnd.microsoft.icon'
            elif TypeInfo == '.ics':
                TypeInfo = 'text/calendar'
            elif TypeInfo == '.jar':
                TypeInfo = 'application/java-archive'
            elif TypeInfo == '.jpeg':
                TypeInfo = 'image/jpeg'
            elif TypeInfo == '.js':
                TypeInfo = 'text/javascript'
            elif TypeInfo == '.json':
                TypeInfo = 'application/json'
            elif TypeInfo == '.jsonld':
                TypeInfo = 'application/ld+json'
            elif TypeInfo == '.mid':
                TypeInfo = 'audio/midi'
            elif TypeInfo == '.midi':
                TypeInfo = 'audio/x-midi'
            elif TypeInfo == '.mjs':
                TypeInfo = 'text/javascript'
            elif TypeInfo == '.mp3':
                TypeInfo = 'audio/mpeg'
            elif TypeInfo == '.mpeg':
                TypeInfo = 'video/mpeg'
            elif TypeInfo == '.mpkg':
                TypeInfo = 'application/vnd.apple.installer+xml'
            elif TypeInfo == '.odp':
                TypeInfo = 'application/vnd.oasis.opendocument.presentation'
            elif TypeInfo == '.odt':
                TypeInfo = 'application/vnd.oasis.opendocument.text'
            elif TypeInfo == '.oga':
                TypeInfo = 'audio/ogg'
            elif TypeInfo == '.ogv':
                TypeInfo = 'video/ogg'
            elif TypeInfo == '.ogx':
                TypeInfo = 'application/ogg'
            elif TypeInfo == '.otf':
                TypeInfo = 'font/otf'
            elif TypeInfo == '.png':
                TypeInfo = 'image/png'
            elif TypeInfo == '.pdf':
                TypeInfo = 'application/pdf'
            elif TypeInfo == '.ppt':
                TypeInfo = 'application/vnd.ms-powerpoint'
            elif TypeInfo == '.pptx':
                TypeInfo = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
            elif TypeInfo == '.rar':
                TypeInfo = 'application/x-rar-compressed'
            elif TypeInfo == '.rtf':
                TypeInfo = 'application/rtf'
            elif TypeInfo == '.sh':
                TypeInfo = 'application/x-sh'
            elif TypeInfo == '.svg':
                TypeInfo = 'image/svg+xml'
            elif TypeInfo == '.swf':
                TypeInfo = 'application/x-shockwave-flash'
            elif TypeInfo == '.tar':
                TypeInfo = 'application/x-tar'
            elif TypeInfo == '.tiff':
                TypeInfo = 'image/tiff'
            elif TypeInfo == '.ttf':
                TypeInfo = 'font/ttf'
            elif TypeInfo == '.txt':
                TypeInfo = 'text/plain'
            elif TypeInfo == '.vsd':
                TypeInfo = 'application/vnd.visio'
            elif TypeInfo == '.wav':
                TypeInfo = 'audio/wav'
            elif TypeInfo == '.weba':
                TypeInfo = 'audio/webm'
            elif TypeInfo == '.webm':
                TypeInfo = 'video/webm'
            elif TypeInfo == '.webp':
                TypeInfo = 'image/webp'
            elif TypeInfo == '.woff':
                TypeInfo = 'font/woff'
            elif TypeInfo == '.woff2':
                TypeInfo = 'font/woff2'
            elif TypeInfo == '.xhtml':
                TypeInfo = 'application/xhtml+xml'
            elif TypeInfo == '.xls':
                TypeInfo = 'application/vnd.ms-excel'
            elif TypeInfo == '.xlsx':
                TypeInfo = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            elif TypeInfo == '.xml':
                TypeInfo = 'application/xml'
            elif TypeInfo == '.xul':
                TypeInfo = 'application/vnd.mozilla.xul+xml'
            elif TypeInfo == '.zip':
                TypeInfo = 'application/zip'
            elif TypeInfo == '.3gp':
                TypeInfo = 'audio/3gpp'
            elif TypeInfo == '.3g2':
                TypeInfo = 'audio/3gpp2'
            elif TypeInfo == '.7z':
                TypeInfo = 'application/x-7z-compressed'
            else:
                TypeInfo = ''
        return TypeInfo