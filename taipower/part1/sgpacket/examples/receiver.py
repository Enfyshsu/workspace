import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sgpacket
import time
import cmd

# example receiver
class SGPacketHelper(cmd.Cmd):
    intro = 'Use the helper to send packets. Type help or ? to list commands.\n'
    prompt = '<Cmd> '

    def do_TCP(self, arg):
        '''********************\nOpen TCP receiver\n********************'''
        port = 7000
        r = sgpacket.Receiver(sgpacket.PacketType.TCP, ip = '0.0.0.0', port = port)
        open_receiver(r, 'TCP', port)
    
    def do_UDP(self, arg):
        '''********************\nOpen UDP receiver\n********************'''
        port = 7001
        r = sgpacket.Receiver(sgpacket.PacketType.UDP, ip = '0.0.0.0', port = port)
        open_receiver(r, 'UDP', port)

    def do_MMS(self, arg):
        '''********************\nOpen MMS receiver\n********************'''
        port = 102
        r = sgpacket.Receiver(sgpacket.PacketType.MMS, ip = '0.0.0.0', port = port)
        open_receiver(r, 'MMS', port)

    def do_DNP3(self, arg):
        '''********************\nOpen DNP3 receiver\n********************'''
        port = 20000
        r = sgpacket.Receiver(sgpacket.PacketType.DNP3, ip = '0.0.0.0', port = port)
        open_receiver(r, 'DNP3', port)

    def do_XMPP(self, arg):
        '''********************\nOpen XMPP receiver\n********************'''
        port = 5222
        r = sgpacket.Receiver(sgpacket.PacketType.XMPP, ip = '0.0.0.0', port = port)
        open_receiver(r, 'XMPP', port)

    def do_bye(self, arg):
        'Exit the helper:  bye'
        print('Bye.')
        return True

def open_receiver(r, pkt_type, port=None):
    try:
        r.run()
        time.sleep(20)
        r.stop()
        receiver_closed(pkt_type, port)
    except:
        r.stop()
        print('Receiver stopped.')

def receiver_closed(pkt_type, port=None):
    print('%s receiver on port %s is closed.' %(pkt_type, port))

if __name__ == '__main__':
    SGPacketHelper().cmdloop()