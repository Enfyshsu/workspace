import socket
import threading
import queue
import enum
import time
from sgpacket.abstract import ITransmitterL3

class UDP_CMD(enum.Enum):
   send = 0
   stop = 1
   
class Client(ITransmitterL3):
    def __init__(self, server_ip = '127.0.0.1', port = 7000):
        self.server_ip = server_ip
        self.port = port
        self.command_q = queue.Queue()
        self.th = None
            
    def _start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        while True:
            if not self.command_q.empty():
                cmd = self.command_q.get()
                if cmd == UDP_CMD.send:
                    msg = self.command_q.get()
                    s.sendto(msg.encode(), (self.server_ip, self.port))
                    print('Send to ' + str(self.server_ip) + ': ' + msg)
                elif cmd == UDP_CMD.stop:
                    s.close()
                    print("Connection closed.")
                    break
            
    def run(self):
        self.th = threading.Thread(target = self._start)
        self.th.start()
        
    def stop(self):
        self.command_q.put(UDP_CMD.stop)
        
    def send_msg(self, msg):
        self.command_q.put(UDP_CMD.send)
        self.command_q.put(msg)
        
    def set_server_ip(self, ip):
        self.server_ip = ip
    
    def set_server_port(self, port):
        self.port = port
        
    def join(self):
        self.th.join()
        
    def send_one(self):
        self.send_msg("ok you are UDP master")

