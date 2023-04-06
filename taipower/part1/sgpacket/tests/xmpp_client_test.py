import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sgpacket.xmpp
import time

client = sgpacket.xmpp.Client()

client.run()

for i in range(5):
    client.send_msg("Edward", "hehehe")
    time.sleep(1)

client.stop()
