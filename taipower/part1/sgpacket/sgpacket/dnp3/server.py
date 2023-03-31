from pydnp3 import opendnp3
from ._outstation import Outstation
import threading
from sgpacket.abstract import IReceiver

class Server(IReceiver):
    def __init__(self, local_ip = "0.0.0.0", port = 20000):
        self.log_levels = opendnp3.levels.NORMAL | opendnp3.levels.ALL_COMMS
        self.local_ip = local_ip
        self.port = port
        self.close_event = threading.Event()
    
    def _start(self):
        self.app = Outstation(log_levels = self.log_levels, local_ip = self.local_ip, port = self.port)
        self.close_event.wait()
        self.app.shutdown()
        
    def run(self):
        self.close_event.clear()
        th = threading.Thread(target=self._start)
        th.start()
        
    def stop(self):
        self.close_event.set()
    
    def set_ip(self, ip):
        self.local_ip = ip
    
    def set_port(self, port):
        self.port = port