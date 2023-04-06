import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sgpacket.mms
import time

client = sgpacket.mms.Client()

client.run()

time.sleep(3)

for i in range(5):
    client.request_data()
    time.sleep(0.1)

time.sleep(3)

client.stop()