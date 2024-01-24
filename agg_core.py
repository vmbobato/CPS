import socket
import struct


class agg_core_server:
    def __init__(self) -> None:
        self.core_addr = ('172.24.9.34',15001)
        self.server = self.config_server(self.core_addr)
        self.dso_soc, self.dso_addr = self.server.accept()

    def config_server(self, addr):
        ch_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ch_sock.bind(addr)
        ch_sock.listen()
        return ch_sock
    
    def receive_dso(self):
        data = self.dso_soc.recv(1024)
        data = struct.unpack('!iiff', data)
        return data
    

class DER_core:
    def __init__(self) -> None:
        self.der_addr_1 = ('172.24.9.5', 15002)#, ('172.24.9.2', 15003), ('172.24.9.3', 15004), ('172.24.9.4', 15005)]
        self.client_1 = self.config_agg_core_client(self.der_addr_1)

        self.der_addr_2 = ('172.24.9.2', 15003)#, ('172.24.9.2', 15003), ('172.24.9.3', 15004), ('172.24.9.4', 15005)]
        self.client_2 = self.config_agg_core_client(self.der_addr_2)

        self.der_addr_3 = ('172.24.9.3', 15004)#, ('172.24.9.2', 15003), ('172.24.9.3', 15004), ('172.24.9.4', 15005)]
        self.client_3 = self.config_agg_core_client(self.der_addr_3)

        self.der_addr_4 = ('172.24.9.4', 15005)#, ('172.24.9.2', 15003), ('172.24.9.3', 15004), ('172.24.9.4', 15005)]
        self.client_4 = self.config_agg_core_client(self.der_addr_4)

    def config_agg_core_client(self, addr : tuple):
        ch_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ch_sock.connect(addr)
        return ch_sock

    def send_der_core(self, data : list):
        self.client_1.sendto(struct.pack('!iiiffff', *data[0]), self.der_addr_1)
        self.client_2.sendto(struct.pack('!iiiffff', *data[1]), self.der_addr_2)
        self.client_3.sendto(struct.pack('!iiiffff', *data[2]), self.der_addr_3)
        self.client_4.sendto(struct.pack('!iiiffff', *data[3]), self.der_addr_4)

    def receive_der_core(self):
        data = []
        data_1 = self.client_1.recv(7*1024)
        data_2 = self.client_2.recv(7*1024)
        data_3 = self.client_3.recv(7*1024)
        data_4 = self.client_4.recv(7*1024)
        data.append(struct.unpack('!iiiffff', data_1))
        data.append(struct.unpack('!iiiffff', data_2))
        data.append(struct.unpack('!iiiffff', data_3))
        data.append(struct.unpack('!iiiffff', data_4))
        return data



class agg_rtds:
    def __init__(self) -> None:
        self.channel_addr_9 = ('10.125.184.178', 7001)
        self.channel_9 = self.config_channel(self.channel_addr_9)

        self.channel_addr_5 = ('10.125.184.174', 7001)
        self.channel_5 = self.config_channel(self.channel_addr_5)

        self.channel_addr_6 = ('10.125.184.175', 7001)
        self.channel_6 = self.config_channel(self.channel_addr_6)

        self.channel_addr_7 = ('10.125.184.176', 7001)
        self.channel_7 = self.config_channel(self.channel_addr_7)

        self.channel_addr_8 = ('10.125.184.177', 7001)
        self.channel_8 = self.config_channel(self.channel_addr_8)

    def config_channel(self, addr : tuple):
        ch_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ch_sock.connect(addr)
        return ch_sock

    def send_ch9(self, data : list, dst_addr : tuple):
        self.channel_9.sendto(struct.pack('!iiff', *data), dst_addr)

    def receive_ch5_8(self):
        data = []
        data_5 = self.channel_5.recv(7*1024)
        data_6 = self.channel_6.recv(7*1024)
        data_7 = self.channel_7.recv(7*1024)
        data_8 = self.channel_8.recv(7*1024)
        data.append(struct.unpack('!iiiffff', data_5))
        data.append(struct.unpack('!iiiffff', data_6))
        data.append(struct.unpack('!iiiffff', data_7))
        data.append(struct.unpack('!iiiffff', data_8))
        return data
    
    def send_ch5_8(self, data):
        self.channel_5.sendto(struct.pack('!iiiffff', *data[0]), self.channel_addr_5)
        self.channel_6.sendto(struct.pack('!iiiffff', *data[1]), self.channel_addr_6)
        self.channel_7.sendto(struct.pack('!iiiffff', *data[2]), self.channel_addr_7)
        self.channel_8.sendto(struct.pack('!iiiffff', *data[3]), self.channel_addr_8)


agg_core = agg_core_server()
der_core = DER_core()
rtds = agg_rtds()

#while True:
data = agg_core.receive_dso()
print('------Step 3-------')
print(f'AGG$ Data Received from DSO: {data}\n')
rtds.send_ch9(data, rtds.channel_addr_9)

print('------Step 4-------')
data = rtds.receive_ch5_8()
der_core.send_der_core(data)
print(f'AGG$ Data Sent to All DERs\n')

print('------Step 5-------')
der_response = der_core.receive_der_core()
print(f'AGG$ Data Received from DER: {der_response}\n')
rtds.send_ch5_8(der_response)

print('------Step 7-------')
data = rtds.receive_ch5_8()
der_core.send_der_core(data)
print(f'AGG$ Data Sent to DERs\n')

print('------Step 8-------')
der_response = der_core.receive_der_core()
print(f'AGG$ Data Received from DER: {der_response}\n')
rtds.send_ch5_8(der_response)



