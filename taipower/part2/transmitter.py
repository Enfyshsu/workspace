import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../sgpacket')))
from sgpacket import tcp, udp
import time
import random, string
import cmd
import argparse

def get_args():
    parser = argparse.ArgumentParser() 
    parser.add_argument('--pkt_type', '-t', type=str, required=False, help='Transmitter packet type')
    parser.add_argument('--start_time', '-st', type=int, default=0, required=False, help='Transmitter start time (sec)')
    parser.add_argument('--last_time', '-lt', type=int, default=5, required=False, help='Transmitter last time (sec)')
    parser.add_argument('--addr', '-a', type=str, default='10.0.1.201', required=False, help='Transmitter last time (sec)')
    return parser.parse_args()

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

def transmit_specific_packet(pkt_type, st, lt, addr):
    if(pkt_type == 'XMPP'):
        port = 5222
        padding = ''.join(random.choice(string.ascii_letters) for x in range(317))
        sleep_time = 0.05
        t = tcp.Client(server_ip = addr, port = port)
    elif(pkt_type == 'DNP3'):
        port = 20000
        padding = ''.join(random.choice(string.ascii_letters) for x in range(467))
        sleep_time = 0.05
        t = tcp.Client(server_ip = addr, port = port)
    elif(pkt_type == 'UDP'):
        port = 7001
        padding = ''.join(random.choice(string.ascii_letters) for x in range(1367))
        sleep_time = 0.0005
        t = udp.Client(server_ip = addr, port = port)
    else:
        print('No service.')
        return
    
    try:
        time.sleep(st)
        t.run()
        curr_time = time.time()
        while True:
            if(time.time() < curr_time + lt):
                t.send_msg("<time> " + str('%.6f' % time.time()) + " </time> " + padding)
                time.sleep(sleep_time)
            else:
                break
        t.stop()
        t.join()
        sent_success(pkt_type, addr, port)
    except:
        t.stop()
        print('Transmitter stopped.')

if __name__ == '__main__':
    args = get_args()
    if args.pkt_type:
        transmit_specific_packet(args.pkt_type, args.start_time, args.last_time, args.addr)
    else:
        SGPacketHelper().cmdloop()