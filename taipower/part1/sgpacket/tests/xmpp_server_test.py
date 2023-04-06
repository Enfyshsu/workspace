import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sgpacket.xmpp
import time

server = sgpacket.xmpp.Server()

server.run()

#time.sleep(15)

#server.stop()
