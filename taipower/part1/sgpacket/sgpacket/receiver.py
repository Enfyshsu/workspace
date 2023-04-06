from .abstract import *
from .packet import PacketType
from . import tcp, udp, dnp3, mms, xmpp

class Receiver(IReceiver):
    def __init__(self, packet_type, ip, port):
        self.packet_type = packet_type
        self.handler = None
    
        if self.packet_type == PacketType.TCP:
            self.handler = tcp.Server()
        elif self.packet_type == PacketType.UDP:
            self.handler = udp.Server()
        elif self.packet_type == PacketType.DNP3:
            self.handler = dnp3.Server()
        elif self.packet_type == PacketType.MMS:
            self.handler = mms.Server()
        elif self.packet_type == PacketType.XMPP:
            self.handler = xmpp.Server()
        else:
            raise NotImplementedError
            
        self.set_ip(ip)
        self.set_port(port)
        
    def run(self):
        self.handler.run()
        
    def stop(self):
        self.handler.stop()
        
    def set_ip(self, ip):
        self.handler.set_ip(ip)
        
    def set_port(self, port):
        self.handler.set_port(port)