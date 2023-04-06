import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sgpacket.dnp3

server = sgpacket.dnp3.Server()

server.run()

#server.stop()