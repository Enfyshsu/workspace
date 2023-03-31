import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sgpacket.udp
import time

server = sgpacket.udp.Server()

server.run()

time.sleep(30)

server.stop()
