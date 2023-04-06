import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sgpacket.tcp
import time

server = sgpacket.tcp.Server()

server.run()

time.sleep(3)

#server.stop()
