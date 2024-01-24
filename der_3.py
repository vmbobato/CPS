import socket
import struct

class DER:
    def __init__(self) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('172.24.9.3', 15004))
        self.server.listen()
        self.agg_soc, self.agg_addr = self.server.accept()

    def receive(self):
        data = self.agg_soc.recv(7*1024)
        data = struct.unpack('!iiiffff', data)
        return data

    def send(self, data):
        msg = struct.pack('!iiiffff', *data)
        self.agg_soc.sendto(msg, self.agg_addr)


class DER_rtds:
    def __init__(self) -> None:
        self.channel_addr = ('10.125.184.172', 7001)
        self.channel = self.config_channel(self.channel_addr)

    def config_channel(self, addr : tuple):
        ch_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ch_sock.connect(addr)
        return ch_sock

    def send_ch(self, data : list, dst_addr : tuple):
        self.channel.sendto(struct.pack('!iiiffff', *data), dst_addr)

    def receive_ch(self):
        data = self.channel.recv(7*1024)
        data = struct.unpack('!iiiffff', data)
        return data


der = DER()
rtds = DER_rtds()

data_main = der.receive()

print('------Step 4-------')
print(f'DER$ Data received from Agg: {data_main}\n')
rtds.send_ch(data_main, rtds.channel_addr)

print('------Step 5-------')
data = rtds.receive_ch()
print(f'DER$ Data Sent to Agg\n')
der.send(data)

data_main = der.receive()
print('------Step 7-------')
print(f'DER$ Data received from Agg: {data_main}\n')
rtds.send_ch(data_main, rtds.channel_addr)

print('------Step 8-------')
data = rtds.receive_ch()
print(f'DER$ Data Sent to Agg\n')
der.send(data_main)