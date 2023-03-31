import socket
import threading
import time
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
        # if len(self.time_log):
        #     self.delay_analysis(self.time_log)

    def set_ip(self, ip):
        self.host = ip
        
    def set_port(self, port):
        self.port = port
    
    def set_psize(self, psize):
        self.psize = psize
        
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
                self.time_log.append(time.time() - float(to_parse.split()[1]))
                print(len(self.time_log))
            # print(len(to_parse), flush = True)
            # print(len(pkt), flush = True)
            
    def delay_analysis(self, data):
        mean = np.mean(data)
        std = np.std(data)
        print("Mean: %.6f" %mean) 
        print("Standard Deviation: %.6f" % std)