from . import _lib61850
from sgpacket.abstract import *
import time
import threading
import codecs
import queue
import enum
from sgpacket.abstract import ITransmitterL2

class SV_CMD(enum.Enum):
   send = 0
   stop = 1
   
class Publisher(ITransmitterL2):
    def __init__(self, interface = 'eth0'):
        self.interface = interface
        self.command_q = queue.Queue()
        
        self.CommParameters = _lib61850.CommParameters()
        self.CommParameters.appId = 1000
        # Set dst mac here OwO
        self.CommParameters.dstAddress[0] = 0x01
        self.CommParameters.dstAddress[1] = 0x02
        self.CommParameters.dstAddress[2] = 0x03
        self.CommParameters.dstAddress[3] = 0x04
        self.CommParameters.dstAddress[4] = 0x05
        self.CommParameters.dstAddress[5] = 0x06
        self.CommParameters.vlanId = 0
        self.CommParameters.vlanPriority = 5
        self.th = None
    def _start(self):
        svPublisher = _lib61850.SVPublisher_create(self.CommParameters, self.interface)
        if svPublisher:
            asdu1 = _lib61850.SVPublisher_addASDU(svPublisher, "svpub1", None, 1)
            float1 = _lib61850.SVPublisher_ASDU_addFLOAT(asdu1)
            float2 = _lib61850.SVPublisher_ASDU_addFLOAT(asdu1)
            ts1 = _lib61850.SVPublisher_ASDU_addTimestamp(asdu1)
        
            _lib61850.SVPublisher_setupComplete(svPublisher)
            fVal1 = 1234.5678
            fVal2 = 0.12345
            
            while True:
                if not self.command_q.empty():
                    cmd = self.command_q.get()
                    if cmd == SV_CMD.send:
                        ts = _lib61850.Timestamp()
                        _lib61850.Timestamp_clearFlags(ts)
                        _lib61850.Timestamp_setTimeInMilliseconds(ts, int(time.time()))
                        
                        _lib61850.SVPublisher_ASDU_setFLOAT(asdu1, float1, fVal1)
                        _lib61850.SVPublisher_ASDU_setFLOAT(asdu1, float2, fVal2)
                        _lib61850.SVPublisher_ASDU_setTimestamp(asdu1, ts1, ts)
                
                        _lib61850.SVPublisher_ASDU_increaseSmpCnt(asdu1);
                        fVal1 += 1.1
                        fVal2 += 0.1
                        _lib61850.SVPublisher_publish(svPublisher)
                        #time.sleep(0.5)
                    elif cmd == SV_CMD.stop:
                        break
            _lib61850.SVPublisher_destroy(svPublisher)
        else:
            print("Failed to create SV publisher.")
    def run(self):
        self.th = threading.Thread(target=self._start)
        self.th.start()
    
    def publish_data(self):
        self.command_q.put(SV_CMD.send)
        
    def stop(self):
        self.command_q.put(SV_CMD.stop)
    
    def set_ifce(self, interface):
        self.interface = interface
    
    def set_dst_mac(self, dst_mac):
        assert len(dst_mac) == 12
        dst_mac = codecs.decode(dst_mac, 'hex')
        assert len(dst_mac) == 6
        self.CommParameters.dstAddress[0] = dst_mac[0]
        self.CommParameters.dstAddress[1] = dst_mac[1]
        self.CommParameters.dstAddress[2] = dst_mac[2]
        self.CommParameters.dstAddress[3] = dst_mac[3]
        self.CommParameters.dstAddress[4] = dst_mac[4]
        self.CommParameters.dstAddress[5] = dst_mac[5]
    
    def send_one(self):
        self.publish_data()

    def join(self):
        self.th.join()

