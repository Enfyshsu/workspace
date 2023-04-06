import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sgpacket.dnp3
import time
client = sgpacket.dnp3.Client()
client.run()
time.sleep(3)
client.send_o1()
time.sleep(3)
client.send_o2()
time.sleep(3)
client.send_o3()
time.sleep(3)
client.stop()
