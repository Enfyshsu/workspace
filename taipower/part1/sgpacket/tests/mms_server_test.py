import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sgpacket.mms
import time

server = sgpacket.mms.Server()

server.run()

time.sleep(3)

server.set_attr_val(20)

time.sleep(30)

server.stop()