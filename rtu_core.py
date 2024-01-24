import socket
import struct

class RTU_RTDS:
    def __init__(self) -> None:
        self.channel_addr = ('10.125.184.183', 7001)
        self.channel = self.config_channel(self.channel_addr)
        print('[.] RTU - RTDS Comm is UP')

    def config_channel(self, addr : tuple):
        ch_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ch_sock.connect(addr)
        return ch_sock

    # channel 1 - receive only
    def receive_ch1(self):
        data = self.channel.recv(7*1024)
        data = struct.unpack('!iiff', data)
        print(f"CH1 Data Received: {data}")
        return data

    def close(self):
        self.channel.close()


class RTU_CORE:
    def __init__(self) -> None:
        self.dso_addr = ('172.24.9.18', 15000)
        self.rtu = self.config_channel(self.dso_addr)

    def config_channel(self, addr : tuple):
        ch_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ch_sock.connect(addr)
        print('RTU - CORE is Connected to DSO CORE')
        return ch_sock

    def send_dso(self, data : list, dst_addr : tuple):
        self.rtu.sendto(struct.pack('!iiff', *data), dst_addr)

    def close(self):
        self.rtu.close()


rtds = RTU_RTDS()
rtu = RTU_CORE()

#while True:
data = rtds.receive_ch1()
rtu.send_dso(data, rtu.dso_addr)
print('-----Step 1.a)-----')
print('RTU$ DATA SENT to DSO\n')