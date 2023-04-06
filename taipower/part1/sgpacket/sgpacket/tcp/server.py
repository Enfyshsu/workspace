import socket
import threading
import time
import os
import numpy as np
from sgpacket.abstract import IReceiver

class Server(IReceiver):
    def __init__(self, host = '0.0.0.0', port = 7000):
        self.host = host
        self.port = port
        self.conn = None
        self.s = None
        self.time_log = []
        self.psize = None
        self.pkt_type = None
        
    def _start(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host, self.port))
        self.s.listen(5)

        print('wait for connection...')
        
        # self.conn, addr = self.s.accept()
        # print('connected by ' + str(addr))

        if self.psize:
            while True:
                self.conn, addr = self.s.accept()
                thread = threading.Thread(target = self.msg_handle, args = (self.conn, addr))
                thread.setDaemon(True)
                thread.start()
        else:
            while True:
                self.conn, addr = self.s.accept()
                while True:
                    indata = self.conn.recv(1024)
                    if len(indata) == 0: # connection closed
                        self.conn.close()
                        break
                    print('recv: ' + indata.decode())

        print('Client closed connection.')
        
    def set_ip(self, ip):
        self.host = ip
        
    def set_port(self, port):
        self.port = port
    
    def set_psize(self, psize):
        self.psize = psize
    
    def set_pkt_type(self, pkt_type):
        self.pkt_type = pkt_type
        
    def run(self):
        th = threading.Thread(target = self._start)
        th.start()
        
    def stop(self):
        self.s.close()
        if len(self.time_log):
            print(len(self.time_log))
            self.delay_analysis(self.time_log)

    def msg_handle(self, conn, addr):
        pkt = b''
        while True:
            indata = conn.recv(self.psize)
            if len(indata) == 0: # connection closed
                conn.close()
                break
            pkt += indata
            to_parse = b''
            if len(pkt) >= self.psize:
                to_parse = pkt[:self.psize]
                pkt = pkt[self.psize:]
                curr_time = time.time()
                self.time_log.append((curr_time, curr_time - float(to_parse.split()[1])))
                print(len(self.time_log))
            
    def delay_analysis(self, data):
        latency = np.array(data)[:, 1]
        mean = np.mean(latency)
        std = np.std(latency)
        print("Mean: %.6f" %mean) 
        print("Standard Deviation: %.6f" % std)

        np.save('/sgpacket/log/' + self.pkt_type + '_' + str(time.time())[:10], data)