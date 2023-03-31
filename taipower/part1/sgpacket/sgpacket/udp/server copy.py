import socket
import threading 
import time
import statistics
from sgpacket.abstract import IReceiver

class Server(IReceiver):
    def __init__(self, host = '0.0.0.0', port = 7000):
        self.host = host
        self.port = port
        self.s = None
        self.packet_num = None
        self.time_log = []
        
    def _start(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host, self.port))
        print('Wait for data...')
        while True:
            indata, addr = self.s.recvfrom(1024)
            if indata.find('<time>'.encode('utf-8')) >= 0:
                self.time_log.append(time.time() - float(indata.split()[1]))
            print('Receive data from ' + str(addr) + ': ' + indata.decode())
        print('Client closed connection.')
        # self.delay_analysis(self.time_log)
        
    def run(self):
        th = threading.Thread(target = self._start)
        th.start()
        
    def stop(self):
        self.s.close()
        if len(self.time_log) == self.packet_num:
            self.delay_analysis(self.time_log)
    
    def set_ip(self, ip):
        self.host = ip
    
    def set_port(self, port):
        self.port = port
        
    def delay_analysis(self, data):
        mean = statistics.mean(data)
        stdev = statistics.stdev(data)
        print("Mean: %.6f" %mean) 
        print("Standard Deviation: %.6f" % stdev)