import sys
sys.path.insert(0, "/libiec61850/pyiec61850")
import iec61850
import time
import queue
import threading
import enum
import codecs
from sgpacket.abstract import ITransmitterL2

class GOOSE_CMD(enum.Enum):
   send = 0
   stop = 1
   
class Publisher(ITransmitterL2):
    def __init__(self, interface = 'eth0'):
        self.dataSetValues = iec61850.LinkedList_create()
        iec61850.LinkedList_add(self.dataSetValues, iec61850.MmsValue_newIntegerFromInt32(1234))
        iec61850.LinkedList_add(self.dataSetValues, iec61850.MmsValue_newBinaryTime(False))
        iec61850.LinkedList_add(self.dataSetValues, iec61850.MmsValue_newIntegerFromInt32(5678))
        
        self.gooseCommParameters = iec61850.CommParameters()
        self.gooseCommParameters.appId = 1000
        # Set dst mac here OwO
        iec61850.CommParameters_setDstAddress(self.gooseCommParameters, 0x01, 0x0c, 0xcd, 0x01, 0x00, 0x01)
        self.gooseCommParameters.vlanId = 0
        self.gooseCommParameters.vlanPriority = 5
        
        self.interface = interface
        self.command_q = queue.Queue()
        self.th = None
        
    def _start(self):
        publisher = iec61850.GoosePublisher_create(self.gooseCommParameters, self.interface)
        if publisher:
            iec61850.GoosePublisher_setGoCbRef(publisher, "simpleIOGenericIO/LLN0$GO$gcbAnalogValues")
            iec61850.GoosePublisher_setConfRev(publisher, 1)
            iec61850.GoosePublisher_setDataSetRef(publisher, "simpleIOGenericIO/LLN0$AnalogValues")
            iec61850.GoosePublisher_setTimeAllowedToLive(publisher, 500)
            
            while True:
                if not self.command_q.empty():
                    cmd = self.command_q.get()
                    if cmd == GOOSE_CMD.send:
                        res = iec61850.GoosePublisher_publish(publisher, self.dataSetValues)
                        if res == -1:
                            print("Error sending message")
                    elif cmd == GOOSE_CMD.stop:
                        break
                        
            iec61850.GoosePublisher_destroy(publisher)
        else:
            print("Failed to create GOOSE publisher.")
            iec61850.LinkedList_destroyDeep(self.dataSetValues, iec61850.MmsValue_delete)
    
    def run(self):
        self.th = threading.Thread(target=self._start)
        self.th.start()
    
    def publish_data(self):
        self.command_q.put(GOOSE_CMD.send)
        
    def stop(self):
        self.command_q.put(GOOSE_CMD.stop)

    def set_ifce(self, interface):
        self.interface = interface
    
    def set_dst_mac(self, dst_mac):
        assert len(dst_mac) == 12
        dst_mac = codecs.decode(dst_mac, 'hex')
        assert len(dst_mac) == 6
        iec61850.CommParameters_setDstAddress(self.gooseCommParameters, dst_mac[0], dst_mac[1], dst_mac[2], dst_mac[3], dst_mac[4], dst_mac[5])
        
    def send_one(self):
        self.publish_data()
    
    def join(self):
        self.th.join()