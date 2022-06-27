from Controller.BaseController import *

CodeExecRouter = APIRouter()
CodeExecPrefix = ''

_common: Common = Common()
_file: FileHelper = FileHelper()
_lang: Lang = Lang()


# 考生代码执行
@CodeExecRouter.post('/Code/Exec')
async def CodeExec(
        request: Request,
        Key: str = Form(''),
        Language: str = Form(''),
        Version: str = Form(''),
        CodeStr: str = Form(''),
        RandomStr: str = Form(''),
) -> Result:
    return CodeExecAction(Key.strip(), Language.strip(), Version.strip(), CodeStr.strip(), RandomStr.strip())


# 测试
@CodeExecRouter.post('/Code/Exec/Test')
async def CodeExec(
        request: Request,
        Key: str = Form(''),
        Language: str = Form(''),
        Version: str = Form(''),
        CodeStr: str = Form(''),
        RandomStr: str = Form(''),
) -> Result:
    CodeStrBytes = CodeStr.strip().encode(encoding="utf-8")
    CodeStr64 = base64.b64encode(CodeStrBytes)
    return CodeExecAction(Key.strip(), Language.strip(), Version.strip(), CodeStr64, RandomStr.strip())


'''
代码执行
Key 秘钥
Language 语言
Version 版本
CodeStr 代码
RandomStr 随机数
'''


def CodeExecAction(
    Key: str,
    Language: str,
    Version: str,
    CodeStr: str,
    RandomStr: str,
) -> Result:
    ServerKey = 'TXNGG3KidItKrCGf5wXT53eZTYCOynOAIjbKJPdy'
    CodeFilePath = getcwd() + '/CodeExec/CodeFile/'  # 模板文件夹
    CodeDir = getcwd() + '/CodeExec/CodeTemp/'  # 代码执行文件夹
    result = Result()

    try:
        _file.MkDir(CodeDir)
    except Exception as e:
        result.Memo = str(e)
        return result

    CheckCliInfo = ''  # 正确答案比对参数

    # print('原始数据:')
    # print(CodeStr)
    # print('.....')

    if CodeStr == '':
        result.Memo = _lang.ParamErr
        return result

    try:
        CodeStr = base64.b64decode(CodeStr).decode('utf-8')
    except OSError as e:
        result.Memo = str(e)
        return result

    # print('解码数据:')
    # print(CodeStr)
    # print('.....')

    if Key != ServerKey:
        result.Memo = _lang.ParamErr
    elif Language == '':
        result.Memo = _lang.ParamErr
    elif Version == '':
        result.Memo = _lang.ParamErr
    elif RandomStr == '':
        result.Memo = _lang.ParamErr
    else:
        Language = Language.lower()

        if Language == 'php':
            TempFile = 'php.php'
        elif Language == 'javascript':
            TempFile = 'javascript.js'
        elif Language == 'python':
            TempFile = 'python.py'
        elif Language == 'java':
            TempFile = 'java.java'
        elif Language == 'c':
            TempFile = 'c.c'
        else:
            TempFile = ''

        if Language == 'php':
            LangSuffix = '.php'
        elif Language == 'javascript':
            LangSuffix = '.js'
        elif Language == 'python':
            LangSuffix = '.py'
        elif Language == 'java':
            LangSuffix = '.java'
        elif Language == 'c':
            LangSuffix = '.c'
        else:
            LangSuffix = ''

        if Language == 'php':
            DockerRun = 'docker run ' + ' --rm -it -v ' + CodeDir + ':/home/code -w /home/code php:' + Version + ' php ' + RandomStr + '.php',
        elif Language == 'javascript':
            DockerRun = 'docker run ' + ' --rm -it -v ' + CodeDir + ':/home/code -w /home/code node node ' + RandomStr + '.js',
        elif Language == 'python':
            DockerRun = 'docker run ' + ' --rm -it -v ' + CodeDir + ':/home/code -w /home/code python:' + Version + ' python ' + RandomStr + '.py',
        elif Language == 'java':
            DockerRun = 'docker run ' + ' --rm -it -v ' + CodeDir + ':/home/code -w /home/code',
        elif Language == 'c':
            DockerRun = 'docker run ' + ' --rm -it -v ' + CodeDir + ':/home/code -w /home/code',
        else:
            DockerRun = ''

        try:
            if LangSuffix != '' and DockerRun != '':
                FilePath = CodeFilePath + TempFile
                f = open(FilePath, 'r')
                FileContent = f.read()
                f.close()

                if FileContent != '':
                    FileContent = FileContent.replace('[CODE]', CodeStr)
                    if Language == 'java':
                        FileContent = FileContent.replace('[NAME]', 'Test' + RandomStr)

                CodeFile = ''  # 代码运行文件
                if Language == 'java':
                    CodeFile = CodeDir + 'Test' + RandomStr + LangSuffix
                else:
                    CodeFile = CodeDir + RandomStr + LangSuffix

                try:
                    file = open(CodeFile, 'w')
                    file.close()
                except OSError as e:
                    result.Memo = str(e)
                    return result

                try:
                    File = open(CodeFile, 'w')
                    File.write(FileContent)
                    File.close()
                except OSError as e:
                    result.Memo = str(e)
                    remove(CodeFile)
                    return result

                if Language == 'java':
                    _common.CLI(DockerRun[0] + ' openjdk:' + Version + ' javac Test' + RandomStr + '.java')
                if Language == 'c':
                    _common.CLI('gcc ' + CodeDir + RandomStr + '.c -o ' + CodeDir + RandomStr)

                # print('执行语句:')
                # print(DockerRun[0])
                # print('=====================')

                cliinfo = ''
                try:
                    if Language == 'java':
                        cliinfo = json.loads(_common.CLI(DockerRun[0] + ' openjdk:' + Version + ' java Test' + RandomStr))
                    elif Language == 'c':
                        print(_common.CLI(DockerRun[0] + ' gcc /home/code/' + RandomStr))
                        cliinfo = json.loads(_common.CLI(DockerRun[0] + ' gcc /home/code/' + RandomStr))
                    else:
                        cliinfo = json.loads(_common.CLI(DockerRun[0]))
                except OSError as e:
                    result.Memo = str(e)
                    return result

                CheckCliInfo = cliinfo['Result']

                # print('输出结果字符串 ' + CheckCliInfo)
                # print('==========')

                # 是否有语法错误
                if 'error' in CheckCliInfo:
                    result.Memo = 'error'
                elif 'err' in CheckCliInfo:
                    result.Memo = 'error'
                else:
                    result.Memo = CheckCliInfo

                result.Memo = 'Success'
                result.State = True
                remove(CodeFile)
        except OSError as e:
            result.Memo = str(e)
            return result

    # 删除执行完成的文件(重要)
    if Language == 'java':
        remove(CodeDir + 'Test' + RandomStr + '.class')
        # remove(CodeDir + 'Test' + RandomStr + '.java')

    return result


# 清理执行缓存文件
@CodeExecRouter.get('/Clean/Temp/File')
async def CleanTempFile(request: Request) -> Result:
    result = Result()
    CodeDir = getcwd() + '/CodeExec/CodeTemp/'  # 代码执行文件夹
    try:
        rmtree(CodeDir, ignore_errors=False, onerror=None)
        mkdir(CodeDir)
        result.State = True
    except Exception as e:
        result.Memo = str(e)
    return result