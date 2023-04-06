import sys
sys.path.insert(0, "/libiec61850/pyiec61850")
import iec61850
import time
import threading
import queue
import enum
from sgpacket.abstract import IReceiver

class MMS_SERVER_CMD(enum.Enum):
   set_attr = 0
   stop = 1
   
class Server(IReceiver):
    def __init__(self, port = 102):
        self.port = port
        self.iedModel = iec61850.IedModel_create("testmodel")
        self.ld = iec61850.LogicalDevice_create("LD1", self.iedModel)
        self.ln = iec61850.LogicalNode_create("LN1", self.ld)
        self.do = iec61850.DataObject_create("DO1", iec61850.toModelNode(self.ln), 0)
        self.da = iec61850.DataAttribute_create("data1", iec61850.toModelNode(self.do), iec61850.IEC61850_FLOAT64, iec61850.IEC61850_FC_MX, 0, 0, 0)
        self.iedServer = iec61850.IedServer_create(self.iedModel)
        self.command_q = queue.Queue()
    
    def _start(self):
        iec61850.IedServer_start(self.iedServer, self.port)
        if not iec61850.IedServer_isRunning(self.iedServer):
            print("Starting server failed! Exit.")
            iec61850.IedServer_destroy(self.iedServer)
            
        while True:
            if not self.command_q.empty():
                cmd = self.command_q.get()
                if cmd == MMS_SERVER_CMD.set_attr:
                    val = self.command_q.get()
                    iec61850.IedServer_lockDataModel(self.iedServer);
                    iec61850.IedServer_updateFloatAttributeValue(self.iedServer, self.da, val);
                    iec61850.IedServer_unlockDataModel(self.iedServer);
                elif cmd == MMS_SERVER_CMD.stop:
                    iec61850.IedServer_stop(self.iedServer)
                    iec61850.IedServer_destroy(self.iedServer)
                    break

    def set_attr_val(self, val):
        self.command_q.put(MMS_SERVER_CMD.set_attr)
        self.command_q.put(val)

    def run(self):
        th = threading.Thread(target=self._start)
        th.start()
        self.set_attr_val(87)
        
    def stop(self):
        self.command_q.put(MMS_SERVER_CMD.stop)
        
    def set_ip(self, ip):
        print("WARNING: method set_ip() has not implemented, use 0.0.0.0 instead.")
        pass
        
    def set_port(self, port):
        self.port = port
        
    
