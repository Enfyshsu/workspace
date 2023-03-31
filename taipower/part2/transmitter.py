import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../sgpacket')))
from sgpacket import tcp, udp
import time
import cmd
import random, string

class SGPacketHelper(cmd.Cmd):
    intro = 'Use the helper to send packets. Type help or ? to list commands.\n'
    prompt = '<Cmd> '
    
    def do_XMPP(self, addr):
        '''****************************\nSend XMPP packets: XMPP [IP]\nE.g., XMPP 10.0.1.201\n****************************'''
        port = 5222
        t = tcp.Client(server_ip = addr, port = port)
        padding = ''.join(random.choice(string.ascii_letters) for x in range(317))
        XMPP_NUM = 500
        sleep_time = 0.05
        send_packets(t, 'XMPP', addr, port, padding, XMPP_NUM, sleep_time)
    
    def do_DNP3(self, addr):
        '''****************************\nSend DNP3 packets: DNP3 [IP]\nE.g., DNP3 10.0.1.201\n****************************'''
        port = 20000
        t = tcp.Client(server_ip = addr, port = port)
        padding = ''.join(random.choice(string.ascii_letters) for x in range(467))
        DNP3_NUM = 500
        sleep_time = 0.05
        send_packets(t, 'DNP3', addr, port, padding, DNP3_NUM, sleep_time)

    def do_UDP(self, addr):
        '''****************************\nSend UDP packets: UDP [IP]\nE.g., UDP 10.0.1.201\n****************************'''
        port = 7001
        padding = ''.join(random.choice(string.ascii_letters) for x in range(1367))
        t = udp.Client(server_ip = addr, port = port)
        UDP_NUM = 1000
        sleep_time = 0.0005
        send_packets(t, 'UDP', addr, port, padding, UDP_NUM, sleep_time)

    def do_bye(self, arg):
        'Exit the helper:  bye'
        print('Bye.')
        return True

def send_packets(t, pkt_type, addr, port, padding, p_num, sleep_time):
    try:
        t.run()
        for i in range(p_num):
            t.send_msg("<time> " + str('%.6f' % time.time()) + " </time> " + padding)
            time.sleep(sleep_time)
        t.stop()
        t.join()
        sent_success(pkt_type, addr, port)
    except:
        t.stop()
        print('Transmitter stopped.')

def sent_success(pkt_type, addr, port):
    print('Sent %s packets to %s:%d.' %(pkt_type, addr, port))

if __name__ == '__main__':
    SGPacketHelper().cmdloop()
