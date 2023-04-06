import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sgpacket.tcp
import time

client = sgpacket.tcp.Client()

client.run()

time.sleep(3)

client.send_msg('test')
client.send_one()

time.sleep(3)

client.stop()
