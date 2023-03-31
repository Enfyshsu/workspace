import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sgpacket.udp
import time

client = sgpacket.udp.Client()

client.run()

time.sleep(3)

client.send_msg('test')

time.sleep(3)

client.stop()
