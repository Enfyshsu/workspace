import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../sgpacket')))
from sgpacket import tcp, udp
import time
import cmd
import argparse

def get_args():
    parser = argparse.ArgumentParser() 
    parser.add_argument('--pkt_type', '-t', type=str, required=False, help='Receiver packet type')
    parser.add_argument('--start_time', '-st', type=int, default=0, required=False, help='Receiver start time (sec)')
    parser.add_argument('--last_time', '-lt', type=int, default=180, required=False, help='Receiver last time (sec)')
    return parser.parse_args()

class SGPacketHelper(cmd.Cmd):
    intro = 'Use the helper to send packets. Type help or ? to list commands.\n'
    prompt = '<Cmd> '
    
    def do_XMPP(self, arg):
        '''********************\nOpen XMPP receiver\n********************'''
        port = 5222
        r = tcp.Server(host = '0.0.0.0', port = port)
        XMPP_PSIZE = 350
        open_receiver(r, 'XMPP', port, XMPP_PSIZE)

    def do_DNP3(self, arg):
        '''********************\nOpen DNP3 receiver\n********************'''
        port = 20000
        r = tcp.Server(host = '0.0.0.0', port = port)
        DNP3_PSIZE = 500
        open_receiver(r, 'DNP3', port, DNP3_PSIZE)

    def do_UDP(self, arg):
        '''********************\nOpen UDP receiver\n********************'''
        port = 7001
        r = udp.Server(host = '0.0.0.0', port = port)
        UDP_PSIZE = 1400
        open_receiver(r, 'UDP', port, UDP_PSIZE)

    def do_bye(self, arg):
        'Exit the helper:  bye'
        print('Bye.')
        return True

def open_receiver(r, pkt_type, port, psize):
    try:
        r.psize = psize
        r.pkt_type = pkt_type
        r.run()
        time.sleep(180)
        r.stop()
        receiver_closed(pkt_type, port)
    except:
        r.stop()
        print('Receiver stopped.')

def receiver_closed(pkt_type, port):
    print('%s receiver on port %s is closed.' %(pkt_type, port))

def receive_specific_packet(pkt_type, st, lt):
    if(pkt_type == 'XMPP'):
        port = 5222
        psize = 350
        r = tcp.Server(host = '0.0.0.0', port = port)
    elif(pkt_type == 'DNP3'):
        port = 20000
        psize = 500
        r = tcp.Server(host = '0.0.0.0', port = port)
    elif(pkt_type == 'UDP'):
        port = 7001
        psize = 1400
        r = udp.Server(host = '0.0.0.0', port = port)
    else:
        print('No service.')
        return
    
    try:
        r.psize = psize
        r.pkt_type = pkt_type
        r.run()
        time.sleep(lt)
        r.stop()
        receiver_closed(pkt_type, port)
    except:
        r.stop()
        print('Receiver stopped.')
    
if __name__ == '__main__':
    args = get_args()
    if args.pkt_type:
        receive_specific_packet(args.pkt_type, args.start_time, args.last_time)
    else:
        SGPacketHelper().cmdloop()