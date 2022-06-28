# -*- coding:utf-8 -*-
from Service.BaseService import *
from Service.Common import *


class UDPTool(BaseService):

    def __init__(self, PORT=5002, BUFSIZE=64, SendInfoStr='bitbox', TimeoutSet=15):
        super().__init__()
        HOST = '192.168.' + \
            str(Common().Explode('.', Common().LocalIP())[2]) + '.255'
        self.PORT = PORT
        self.BUFSIZE = BUFSIZE
        self.SendInfoStr = SendInfoStr
        self.ADDR = (HOST, PORT)
        self.UDPClient = socket(AF_INET, SOCK_DGRAM)
        self.UDPClient.settimeout(TimeoutSet)

    # 发送广播
    def Send(self):
        self.UDPClient.sendto(self.SendInfoStr.encode('utf8'), self.ADDR)
        self.SendInfoStr, self.ADDR = self.UDPClient.recvfrom(self.BUFSIZE)
        InformationReceived = self.SendInfoStr.decode('utf8')
        self.UDPClient.close()
        return InformationReceived

    # 发送广播(备选方案)
    def UDPBroadcast(self):
        self.UDPClient.setsockopt(SOL_SOCKET, SO_BROADCAST, True)
        while True:  # 发送广播
            sleep(1)
            try:
                self.UDPClient.sendto(self.SendInfoStr.encode('utf8'), self.ADDR)
            except OSError as e:
                print(e)

    # 接收广播
    def Receive(self, HostName, UDPPort):
        ADDR = ('', UDPPort)
        UDPSocket = socket(AF_INET, SOCK_DGRAM)
        UDPSocket.bind(ADDR)
        while True:
            sleep(1)
            try:
                Data, Addr = UDPSocket.recvfrom(1024)
                if HostName in Addr:
                    UDPSocket.close()
                    return Data.decode('UTF8')
            except (KeyboardInterrupt, SyntaxError):
                print(KeyboardInterrupt, SyntaxError)
                raise
            except OSError as e:
                print(e)

    def UDPReceive(self, UDPPort):
        # 1. 创建套接字
        udp_socket = socket(AF_INET, SOCK_DGRAM)
        # 设置请求超时
        udp_socket.settimeout(5)

        # 2. 绑定本机ip和端口
        udp_socket.bind(('', UDPPort))  # 绑定本机的ip和端口(元组类型)  ''表示本机ip

        # 3. 用套接字接收数据 1024表示本次接收的最大字节数。会阻塞代码,直到接收到数据
        recv_data = udp_socket.recvfrom(1024)
        # recv_data这个变量中存储的是一个元组 (接收到的数据，(发送方的ip, port))
        recv_msg = recv_data[0]  # 字节类型 存储接收到的数据
        send_addr = recv_data[1]  # 元组 存储发送方的地址和端口信息

        # 4. 打印接收到的数据 print(recv_data)  # 元组 (接收到的数据，(发送方的ip, port)) decode将字节转成字符串
        # print('%s:%s' % (str(send_addr), recv_msg.decode('UTF8')))
        ServerInfo = recv_msg.decode('UTF8')

        # 5. 关闭套接字
        udp_socket.close()

        return ServerInfo
