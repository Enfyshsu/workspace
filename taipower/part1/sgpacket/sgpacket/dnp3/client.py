import enum
import queue
import threading
import time
from datetime import datetime
from pydnp3 import opendnp3, openpal
from ._master import Master, MyLogger, AppChannelListener, SOEHandler, MasterApplication
from ._master import command_callback, restart_callback, collection_callback
from sgpacket.abstract import ITransmitterL3

class DNP3_CMD(enum.Enum):
   send_o1 = 0
   send_o2 = 1
   send_o3 = 2
   stop = 3
   
class Client(ITransmitterL3):
    def __init__(self, local_ip = "0.0.0.0", port = 20000, server_ip = "127.0.0.1"):
        self.log_levels = opendnp3.levels.NORMAL | opendnp3.levels.ALL_COMMS
        self.local_ip = local_ip
        self.port = port
        self.server_ip = server_ip
        self.command_q = queue.Queue()
        self.th = None
        # self.transmit_time = None
        
    def _start(self):
        app = Master(log_handler=MyLogger(), listener=AppChannelListener(), soe_handler=SOEHandler(), master_application=MasterApplication(), log_levels = self.log_levels, local_ip = self.local_ip, port = self.port, host_ip = self.server_ip)
        while True:
            cmd = self.command_q.get()
            if cmd == DNP3_CMD.send_o1:
                # app.set_time(time.time())
                # app.send_direct_operate_command(opendnp3.ControlRelayOutputBlock(opendnp3.ControlCode.LATCH_ON), 5, self.calculate_time)
                app.send_direct_operate_command(opendnp3.ControlRelayOutputBlock(opendnp3.ControlCode.LATCH_ON), 5, command_callback)
            elif cmd == DNP3_CMD.send_o2:
                app.send_direct_operate_command(opendnp3.AnalogOutputInt32(7), 10, command_callback)
            elif cmd == DNP3_CMD.send_o3:
                app.send_direct_operate_command_set(opendnp3.CommandSet(
                    [
                        opendnp3.WithIndex(opendnp3.ControlRelayOutputBlock(opendnp3.ControlCode.LATCH_ON), 0),
                        opendnp3.WithIndex(opendnp3.ControlRelayOutputBlock(opendnp3.ControlCode.LATCH_OFF), 1)
                    ]),
                    command_callback
                )
            elif cmd == DNP3_CMD.stop:
                app.shutdown()
                break
            
    def run(self):
        self.th = threading.Thread(target=self._start)
        self.th.start()
        
    def send_o1(self):
        self.command_q.put(DNP3_CMD.send_o1)
        
    def send_o2(self):
        self.command_q.put(DNP3_CMD.send_o2)
    
    def send_o3(self):
        self.command_q.put(DNP3_CMD.send_o3)
        
    def stop(self):
        self.command_q.put(DNP3_CMD.stop)
    
    def join(self):
        self.th.join()
    
    def set_server_ip(self, ip):
        self.server_ip = ip
    
    def set_server_port(self, port):
        self.port = port
    
    def send_one(self):
        self.send_o1()

    # def collection_callback(self, result=None):
    #     """
    #     :type result: opendnp3.CommandPointResult
    #     """
    #     print("Header: {0} | Index:  {1} | State:  {2} | Status: {3}".format(
    #         result.headerIndex,
    #         result.index,
    #         opendnp3.CommandPointStateToString(result.state),
    #         opendnp3.CommandStatusToString(result.status)
    #     ))

    # def calculate_time(self, result=None):
    #     current_time = time.time()
    #     print(current_time - self.transmit_time)
    #     print("Received command result with summary: {}".format(opendnp3.TaskCompletionToString(result.summary)))
    #     print(dir(result))
    #     result.ForeachItem(self.collection_callback)