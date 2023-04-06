from abc import ABC, abstractmethod

class IReceiver(ABC):
    @abstractmethod
    def set_ip(self, ip):
        return NotImplemented
        
    @abstractmethod
    def set_port(self, port):
        return NotImplemented
        
    @abstractmethod
    def run(self):
        return NotImplemented
        
    @abstractmethod
    def stop(self):
        return NotImplemented
        
class ITransmitter(ABC):
    @abstractmethod
    def run(self):
        return NotImplemented
        
    @abstractmethod
    def stop(self):
        return NotImplemented
        
    @abstractmethod
    def send_one(self):
        return NotImplemented
        
    @abstractmethod
    def join(self):
        return NotImplemented

class ITransmitterL2(ITransmitter):
    @abstractmethod
    def set_ifce(self, ifce):
        return NotImplemented
        
    @abstractmethod
    def set_dst_mac(self, dst_mac):
        return NotImplemented

class ITransmitterL3(ITransmitter):
    @abstractmethod
    def set_server_ip(self, server_ip):
        return NotImplemented
        
    @abstractmethod
    def set_server_port(self, server_port):
        return NotImplemented

