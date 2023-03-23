# -*- coding:utf-8 -*-
from Service.BaseService import *


class Result:
    State: bool
    Memo: str
    Code: int
    Data: object

    def __init__(self) -> None:
        super().__init__()
        self.State = False
        self.Memo = ''
        self.Code = 200


class ResultList:
    State: bool
    Memo: str
    Code: int
    Page: int
    PageSize: int
    TotalPage: int
    Data: object

    def __init__(self) -> None:
        super().__init__()
        self.State = False
        self.Memo = ''
        self.Code = 200
        self.Page = 0
        self.PageSize = 0
        self.TotalPage = 0


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

    '''
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
    '''

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
    def LocalIP(self) -> str:
        return '192.168.0.28'
        try:
            s = socket(AF_INET, SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    # 在线获取本地IP
    def LocalIPOnline(self) -> str:
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
            return ''
        else:
            TypeInfo = TypeInfo.lower()
            if TypeInfo == 'audio/aac':
                return '.acc'
            elif TypeInfo == 'application/x-abiword':
                return '.abw'
            elif TypeInfo == 'application/x-freearc':
                return '.arc'
            elif TypeInfo == 'video/x-msvideo':
                return '.avi'
            elif TypeInfo == 'application/vnd.amazon.ebook':
                return '.azw'
            elif TypeInfo == 'application/octet-stream':
                return '.bin'
            elif TypeInfo == 'image/bmp':
                return '.bmp'
            elif TypeInfo == 'application/x-bzip':
                return '.bz'
            elif TypeInfo == 'application/x-bzip2':
                return '.bz2'
            elif TypeInfo == 'application/x-csh':
                return '.csh'
            elif TypeInfo == 'text/css':
                return '.css'
            elif TypeInfo == 'text/csv':
                return '.csv'
            elif TypeInfo == 'application/msword':
                return '.doc'
            elif TypeInfo == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                return '.docx'
            elif TypeInfo == 'application/vnd.ms-fontobject':
                return '.eot'
            elif TypeInfo == 'application/epub+zip':
                return '.epub'
            elif TypeInfo == 'image/gif':
                return '.gif'
            elif TypeInfo == 'text/html':
                return '.html'
            elif TypeInfo == 'image/vnd.microsoft.icon':
                return '.ico'
            elif TypeInfo == 'text/calendar':
                return '.ics'
            elif TypeInfo == 'application/java-archive':
                return '.jar'
            elif TypeInfo == 'image/jpeg':
                return '.jpeg'
            elif TypeInfo == 'text/javascript':
                return '.js'
            elif TypeInfo == 'application/json':
                return '.json'
            elif TypeInfo == 'application/ld+json':
                return '.jsonld'
            elif TypeInfo == 'audio/midi':
                return '.mid'
            elif TypeInfo == 'audio/x-midi':
                return '.midi'
            elif TypeInfo == 'text/javascript':
                return '.mjs'
            elif TypeInfo == 'audio/mpeg':
                return '.mp3'
            elif TypeInfo == 'video/mpeg':
                return '.mpeg'
            elif TypeInfo == 'application/vnd.apple.installer+xml':
                return '.mpkg'
            elif TypeInfo == 'application/vnd.oasis.opendocument.presentation':
                return '.odp'
            elif TypeInfo == 'application/vnd.oasis.opendocument.text':
                return '.odt'
            elif TypeInfo == 'audio/ogg':
                return '.oga'
            elif TypeInfo == 'video/ogg':
                return '.ogv'
            elif TypeInfo == 'application/ogg':
                return '.ogx'
            elif TypeInfo == 'font/otf':
                return '.otf'
            elif TypeInfo == 'image/png':
                return '.png'
            elif TypeInfo == 'application/pdf':
                return '.pdf'
            elif TypeInfo == 'application/vnd.ms-powerpoint':
                return '.ppt'
            elif TypeInfo == 'application/vnd.openxmlformats-officedocument.presentationml.presentation':
                return '.pptx'
            elif TypeInfo == 'application/x-rar-compressed':
                return '.rar'
            elif TypeInfo == 'application/rar':
                return '.rar'
            elif TypeInfo == 'application/rtf':
                return '.rtf'
            elif TypeInfo == 'application/x-sh':
                return '.sh'
            elif TypeInfo == 'image/svg+xml':
                return '.svg'
            elif TypeInfo == 'application/x-shockwave-flash':
                return '.swf'
            elif TypeInfo == 'application/x-tar':
                return '.tar'
            elif TypeInfo == 'image/tiff':
                return '.tiff'
            elif TypeInfo == 'font/ttf':
                return '.ttf'
            elif TypeInfo == 'text/plain':
                return '.txt'
            elif TypeInfo == 'application/vnd.visio':
                return '.vsd'
            elif TypeInfo == 'audio/wav':
                return '.wav'
            elif TypeInfo == 'audio/webm':
                return '.weba'
            elif TypeInfo == 'video/webm':
                return '.webm'
            elif TypeInfo == 'image/webp':
                return '.webp'
            elif TypeInfo == 'font/woff':
                return '.woff'
            elif TypeInfo == 'font/woff2':
                return '.woff2'
            elif TypeInfo == 'application/xhtml+xml':
                return '.xhtml'
            elif TypeInfo == 'application/vnd.ms-excel':
                return '.xls'
            elif TypeInfo == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                return '.xlsx'
            elif TypeInfo == 'application/xml' or TypeInfo == 'text/xml':
                return '.xml'
            elif TypeInfo == 'application/vnd.mozilla.xul+xml':
                return '.xul'
            elif TypeInfo == 'application/zip':
                return '.zip'
            elif TypeInfo == 'video/3gpp' or TypeInfo == 'audio/3gpp':
                return '.3gp'
            elif TypeInfo == 'video/3gpp2' or TypeInfo == 'audio/3gpp2':
                return '.3g2'
            elif TypeInfo == 'application/x-7z-compressed':
                return '.7z'
            else:
                return ''

    # content-type类型查询
    def ContentType(self, TypeInfo: str) -> str:
        if TypeInfo == '':
            return ''
        else:
            TypeInfo = TypeInfo.lower()
            if TypeInfo == '.acc':
                return 'audio/aac'
            elif TypeInfo == '.abw':
                return 'application/x-abiword'
            elif TypeInfo == '.arc':
                return 'application/x-freearc'
            elif TypeInfo == '.avi':
                return 'video/x-msvideo'
            elif TypeInfo == '.azw':
                return 'application/vnd.amazon.ebook'
            elif TypeInfo == '.bin':
                return 'application/octet-stream'
            elif TypeInfo == '.exe':
                return 'application/octet-stream'
            elif TypeInfo == '.bmp':
                return 'image/bmp'
            elif TypeInfo == '.bz':
                return 'application/x-bzip'
            elif TypeInfo == '.bz2':
                return 'application/x-bzip2'
            elif TypeInfo == '.csh':
                return 'application/x-csh'
            elif TypeInfo == '.css':
                return 'text/css'
            elif TypeInfo == '.csv':
                return 'text/csv'
            elif TypeInfo == '.doc':
                return 'application/msword'
            elif TypeInfo == '.docx':
                return 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            elif TypeInfo == '.eot':
                return 'application/vnd.ms-fontobject'
            elif TypeInfo == '.epub':
                return 'application/epub+zip'
            elif TypeInfo == '.gif':
                return 'image/gif'
            elif TypeInfo == '.html':
                return 'text/html'
            elif TypeInfo == '.ico':
                return 'image/vnd.microsoft.icon'
            elif TypeInfo == '.ics':
                return 'text/calendar'
            elif TypeInfo == '.jar':
                return 'application/java-archive'
            elif TypeInfo == '.jpeg':
                return 'image/jpeg'
            elif TypeInfo == '.jpg':
                return 'image/jpeg'
            elif TypeInfo == '.js':
                return 'text/javascript'
            elif TypeInfo == '.json':
                return 'application/json'
            elif TypeInfo == '.jsonld':
                return 'application/ld+json'
            elif TypeInfo == '.mid':
                return 'audio/midi'
            elif TypeInfo == '.midi':
                return 'audio/x-midi'
            elif TypeInfo == '.mjs':
                return 'text/javascript'
            elif TypeInfo == '.mp3':
                return 'audio/mpeg'
            elif TypeInfo == '.mpeg':
                return 'video/mpeg'
            elif TypeInfo == '.mpkg':
                return 'application/vnd.apple.installer+xml'
            elif TypeInfo == '.odp':
                return 'application/vnd.oasis.opendocument.presentation'
            elif TypeInfo == '.odt':
                return 'application/vnd.oasis.opendocument.text'
            elif TypeInfo == '.oga':
                return 'audio/ogg'
            elif TypeInfo == '.ogv':
                return 'video/ogg'
            elif TypeInfo == '.ogx':
                return 'application/ogg'
            elif TypeInfo == '.otf':
                return 'font/otf'
            elif TypeInfo == '.png':
                return 'image/png'
            elif TypeInfo == '.pdf':
                return 'application/pdf'
            elif TypeInfo == '.ppt':
                return 'application/vnd.ms-powerpoint'
            elif TypeInfo == '.pptx':
                return 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
            elif TypeInfo == '.rar':
                return 'application/x-rar-compressed'
            elif TypeInfo == '.rtf':
                return 'application/rtf'
            elif TypeInfo == '.sh':
                return 'application/x-sh'
            elif TypeInfo == '.svg':
                return 'image/svg+xml'
            elif TypeInfo == '.swf':
                return 'application/x-shockwave-flash'
            elif TypeInfo == '.tar':
                return 'application/x-tar'
            elif TypeInfo == '.tiff':
                return 'image/tiff'
            elif TypeInfo == '.ttf':
                return 'font/ttf'
            elif TypeInfo == '.txt':
                return 'text/plain'
            elif TypeInfo == '.vsd':
                return 'application/vnd.visio'
            elif TypeInfo == '.wav':
                return 'audio/wav'
            elif TypeInfo == '.weba':
                return 'audio/webm'
            elif TypeInfo == '.webm':
                return 'video/webm'
            elif TypeInfo == '.webp':
                return 'image/webp'
            elif TypeInfo == '.woff':
                return 'font/woff'
            elif TypeInfo == '.woff2':
                return 'font/woff2'
            elif TypeInfo == '.xhtml':
                return 'application/xhtml+xml'
            elif TypeInfo == '.xls':
                return 'application/vnd.ms-excel'
            elif TypeInfo == '.xlsx':
                return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            elif TypeInfo == '.xml':
                return 'application/xml'
            elif TypeInfo == '.xul':
                return 'application/vnd.mozilla.xul+xml'
            elif TypeInfo == '.zip':
                return 'application/zip'
            elif TypeInfo == '.3gp':
                return 'audio/3gpp'
            elif TypeInfo == '.3g2':
                return 'audio/3gpp2'
            elif TypeInfo == '.7z':
                return 'application/x-7z-compressed'
            elif TypeInfo == '.psd':
                return 'application/x-photoshop'
            elif TypeInfo == '.ico':
                return 'image/x-icon'
            elif TypeInfo == '.wps':
                return 'application/kswps'
            else:
                return ''