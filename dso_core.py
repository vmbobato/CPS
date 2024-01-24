import socket
import struct
import time


class DSO_to_agg_core:
    def __init__(self) -> None:
        self.agg_addr = ('172.24.9.34', 15001)
        self.client = self.config_dso_core_client(self.agg_addr)

    def config_dso_core_client(self, addr : tuple):
        ch_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ch_sock.connect(addr)
        return ch_sock

    def send_agg_core(self, data : list[4]):
        self.client.sendto(struct.pack('!iiff', *data), self.agg_addr)



class DSO_to_RTU:
    def __init__(self) -> None:
        self.dso_server = ('172.24.9.18', 15000)
        self.server = self.config_dso_server(self.dso_server)
        self.dso_soc, self.dso_addr = self.server.accept()

    def config_dso_server(self, addr : tuple):
        ch_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ch_sock.bind(addr)
        ch_sock.listen()
        return ch_sock
    
    def receive_rtu_core(self):
        data = self.dso_soc.recv(7*1024)
        data = struct.unpack('!iiff', data)
        return data
    

class DSO_rtds:
    def __init__(self) -> None:
        self.channel_addr = ('10.125.184.180', 7001)
        self.channel = self.config_channel(self.channel_addr)

    def config_channel(self, addr : tuple):
        ch_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ch_sock.connect(addr)
        return ch_sock

    def send_ch2(self, data : list[4], dst_addr : tuple):
        self.channel.sendto(struct.pack('!iiff', *data), dst_addr)

    def receive_ch2(self):
        data = self.channel.recv(7*1024)
        data = struct.unpack('!iiff', data)
        return data
    

dso_rtu = DSO_to_RTU()
dso_agg= DSO_to_agg_core()
rtds = DSO_rtds()

#while True:
data = dso_rtu.receive_rtu_core()
print('-----Step 1.a)-----')
print(f'DSO$ Data Received from RTU: {data}\n')
rtds.send_ch2(data, rtds.channel_addr)
data = rtds.receive_ch2()

print("Step 2 Internal")

print('------Step 3-------')
dso_agg.send_agg_core(data)
print(f'DSO$ Data Sent to Aggregator.\n')