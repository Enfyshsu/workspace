import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sgpacket.goose
import time

publisher = sgpacket.goose.Publisher()

publisher.run()

time.sleep(3)

for i in range(5):
    publisher.publish_data()
    time.sleep(0.1)

time.sleep(3)

publisher.stop()