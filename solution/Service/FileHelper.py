# -*- coding:utf-8 -*-
from Service.BaseService import *
from Service.Common import *


class FileHelper(BaseService):

    def __init__(self):
        super().__init__()
        self.Common = Common()

    # 根目录
    def BaseDir(self):
        return path[0] + '/'

    # 当前目录
    def CurrentPath(self):
        return abspath(dirname(__file__)) + '/'

    # 新建文件夹
    def MkDir(self, Path):
        if Path != '' and self.DirIsExist(Path) == False:
            mkdir(Path)

    # 创建多路径下的文件夹
    def MkDirs(self, Path):
        if Path != '' and self.DirIsExist(Path) == False:
            makedirs(Path)

    # 文件夹是否存在
    def DirIsExist(self, DirPath):
        return isdir(DirPath)

    # 文件是否存在
    def FileIsExist(self, FilePath):
        return isfile(FilePath)

    # 获取路径下的文件名
    def CheckFileName(self, FilePath):
        if FilePath == '':
            return
        FilePath = FilePath.replace('\\', '/')
        return os.path.splitext(os.path.split(FilePath)[1])[0]

    # 获取文件类型
    def CheckFileType(self, FilePath):
        TypeStr = splitext(FilePath)[-1]
        if len(TypeStr) == 0:
            TypeStr = ''
        return TypeStr.replace('.', '')

    # 获取文件大小(单位: bit)
    def CheckFileSize(self, FilePath):
        return getsize(FilePath)

    # 获取文件MD5
    def CheckFileMD5(self, FilePath):
        md5_value = md5()
        with open(FilePath, 'rb') as file_b:
            while True:
                data_flow = file_b.read(4096)  # 一次读取4G到内存
                if not data_flow:
                    break
                md5_value.update(data_flow)
        file_b.close()
        return md5_value.hexdigest()

    # 遍历文件夹下的文件
    def SelectDirFiles(self, Path=''):
        FileArr = []
        if Path == '':
            return FileArr
        Arr = listdir(Path)
        for i in range(len(Arr)):
            FilePath = Path + '/' + Arr[i]
            if os.path.isfile(FilePath):
                FileArr.append(Arr[i])
        return FileArr

    # 遍历文件夹下的文件夹
    def SelectDirDirs(self, Path=''):
        DirArr = []
        if Path == '':
            return DirArr
        Arr = listdir(Path)
        if len(Arr) > 0:
            for i in range(len(Arr)):
                DirPath = Path + '/' + Arr[i]
                if os.path.isdir(DirPath):
                    DirArr.append(Arr[i])
        return DirArr

    # 递归遍历文件夹
    def SelectDir(self, Path):
        DirList = []
        FileList = []

        i = 0
        j = 0
        for _, dirs, files in walk(Path, topdown=False):
            for name in dirs:
                DirList.append(i)
                DirList[i] = name
                i = i + 1
            for name in files:
                FileList.append(j)
                FileList[j] = name
                j = j + 1

        return DirList, FileList

    # 删除文件和文件夹
    def DirRemoveAll(self, Path):
        rmtree(Path, ignore_errors=False, onerror=None)

    # 删除文件
    def DeleteFile(self, FilePath):
        if self.FileIsExist(FilePath):
            remove(FilePath)
        

    # 新建文件
    def MkFile(self, Path):
        file = open(Path, 'w')
        file.close()

    # 写入文件内容
    def WFile(self, Path, Content):
        File = open(Path, 'w')
        File.write(Content)
        File.close()

    # 二进制方式写入文件内容
    def WFileInByte(self, Path, Content):
        try:
            File = open(Path, 'wb')
            File.write(Content)
            File.close()
        except OSError as e:
            return False
        return True

    '''
    文件读取:
        filePath 文件路径
        start 开始位置
        size 单次读取的字节数
    '''

    def ReadFile(self, filePath, start, size):
        content = ''  # 读取到的内容
        f = open(filePath, 'rb')
        if start == 0:
            f.seek(0, 0)
        else:
            f.seek(start, 1)
        content = f.read(size)
        f.close()
        return content

    '''
    文件切割:
        FilePath 文件路径
        StorageDir 存储路径
        ChunkSize 块大小
    '''

    def CutFile(self, FilePath='', StorageDir='', ChunkSize=0):
        if FilePath == '':
            return False, 0
        if not exists(FilePath):
            return False
        if ChunkSize <= 0:
            return False, 0
        if StorageDir == '':
            return False, 0
        if not exists(StorageDir):
            mkdir(StorageDir)

        Partnum = 0
        try:
            Inputfile = open(FilePath, 'rb')
        except OSError as e:
            return False, 0
        while True:
            Chunk = Inputfile.read(ChunkSize)
            if not Chunk:  # 切割完毕
                break
            Partnum = Partnum + 1
            PartStr = ''
            if Partnum > 0 and Partnum < 10:
                PartStr = 'part.00'
            elif Partnum >= 10 and Partnum < 100:
                PartStr = 'part.0'
            else:
                PartStr = 'part.'
            Filename = join(StorageDir, (PartStr + str(Partnum)))
            Fileobj = open(Filename, 'wb')
            Fileobj.write(Chunk)
            Fileobj.close()
        return True, Partnum

    '''
    文件合并
    FilePartPath 文件分片存放路径
    StorageDir 存储路径
    Filename 合并后的文件名
    '''

    def MergeFile(self, FilePartPath, StorageDir, Filename):
        if StorageDir == '':
            return False
        if Filename == '':
            return False
        if not exists(FilePartPath):
            return False
        Outfile = open(join(StorageDir, Filename), 'wb')
        Files = listdir(FilePartPath)
        Files.sort()
        for File in Files:
            Filepath = join(FilePartPath, File)
            Infile = open(Filepath, 'rb')
            Data = Infile.read()
            Outfile.write(Data)
            Infile.close()
        Outfile.close()
        return True

    # 获取文件信息
    def OSStat(self, FilePath):
        StatInfo = stat(FilePath)
        Data = {}
        Data['st_mode'] = StatInfo[0]
        Data['st_ino'] = StatInfo[1]
        Data['st_dev'] = StatInfo[2]
        Data['st_nlink'] = StatInfo[3]
        Data['st_uid'] = StatInfo[4]
        Data['st_gid'] = StatInfo[5]
        Data['st_size'] = StatInfo[6]
        Data['st_atime'] = StatInfo[7]
        Data['st_mtime'] = StatInfo[8]
        Data['st_ctime'] = StatInfo[9]
        return Data

    # 调用本地系统应用打开文件
    def FileNativeCall(self, FilePath):
        SysType = self.Common.OSType()
        if SysType == 'Windows':
            startfile(FilePath)
        elif SysType == 'Linux':
            call(['xdg-open', FilePath])
        elif SysType == 'MacOS':
            call(['open', FilePath])
        else:
            return

    # windows下设置文件为只读
    def SetReadOnly(self, FilePath):
        osType = self.Common.OSType()
        if osType == 'Windows':
            chmod(FilePath, S_IREAD)
        elif osType == 'MacOS':
            return

    # windows下取消文件只读
    def UnsetReadOnly(self, FilePath):
        osType = self.Common.OSType()
        if osType == 'Windows':
            chmod(FilePath, S_IWRITE)
        elif osType == 'MacOS':
            return

    # 打开本地文件夹
    def OpenLocalDir(self, DirPath):
        os.startfile(DirPath)

    # 设置用户文件夹
    def SetUserDir(self, Account, UploadPath, DownloadPath, BasePath=''):
        if Account == '':
            return False

        # 是否自定义用户根路径
        DefaultPath = os.getcwd()
        if BasePath != '':
            DefaultPath = BasePath

        UploadDirPath = (DefaultPath + '/' + UploadPath + '/Upload_' + Account + '/')  # 设置上传文件夹

        DownloadDirPath = (DefaultPath + '/' + DownloadPath + '/Download_' + Account + '/')  # 设置下载文件夹

        UploadDirPath = UploadDirPath.replace('\\', '/')
        DownloadDirPath = DownloadDirPath.replace('\\', '/')

        self.MkDir(UploadDirPath)  # 新建上传文件夹
        self.MkDir(DownloadDirPath)  # 新建下载文件夹
        return UploadDirPath, DownloadDirPath

    # 下载文件存放目录
    def SetDownloadTempDir(self, Account, DownloadTempPath, BasePath=''):
        if Account == '':
            return False

        # 是否自定义用户根路径
        DefaultPath = os.getcwd()
        if BasePath != '':
            DefaultPath = BasePath
        DownloadTempDir = (DefaultPath + '/' + DownloadTempPath + '/Download_Temp_' + Account + '/')  # 设置下载文件夹
        DownloadTempDir = DownloadTempDir.replace('\\', '/')
        self.MkDir(DownloadTempDir)
        return DownloadTempDir

    # 在线预览临时目录
    def SetTempDir(self, Account, TempPath, BasePath=''):
        if Account == '':
            return False

        # 是否自定义用户根路径
        DefaultPath = os.getcwd()
        if BasePath != '':
            DefaultPath = BasePath
        TempDir = DefaultPath + '/' + TempPath + '/Temp_' + Account + '/'  # 设置下载文件夹
        TempDir = TempDir.replace('\\', '/')
        self.MkDir(TempDir)
        return TempDir

    # 格式化文件大小
    def FileSizeFormat(self, Size=0):
        Size = (int(Size) / 1024) / 1024
        if Size > 1024:
            SizeStr = format(Size / 1024, '.2f') + 'G'
        else:
            SizeStr = format(Size, '.2f') + 'M'
        return SizeStr

    # SourcePath 待压缩文件所在文件目录
    # TargetPath 目标文件目录
    def CompressZip(self, SourcePath, TargetPath):
        if not exists(TargetPath):
            return False
        target = str(int(round(time() * 1000))) + '.zip'
        tarZip = zipfile.ZipFile(target, 'w', zipfile.ZIP_STORED)
        fileList = []
        for root, dirs, files in os.walk(SourcePath):
            for file in files:
                fileList.append(os.path.join(root, file))
        if len(fileList):
            return False
        for filename in fileList:
            tarZip.write(filename, filename[len(SourcePath):])
        tarZip.close()
        return True

    # SourceFile 待解压zip路径
    # TargetPath 目标文件目录
    def Unzip(self, SourceFile, TargetPath):
        try:
            file = zipfile.ZipFile(SourceFile, 'r')
            file.extractall(TargetPath)
        except OSError as e:
            return False
        return True
