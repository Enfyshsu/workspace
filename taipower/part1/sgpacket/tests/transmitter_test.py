import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sgpacket
import time

# test transmitter
t = sgpacket.Transmitter(sgpacket.PacketType.MMS, server_ip = '127.0.0.1', server_port = 102)
# t = sgpacket.Transmitter(sgpacket.PacketType.SV, ifce='lo', dst_mac = '0000dd00aa12')

t.run()
time.sleep(3)
t.send_one()
time.sleep(3)
t.stop()
