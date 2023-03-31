#!/usr/bin/python
"""
This is the most simple example to showcase Containernet.
"""
from mininet.net import Mininet
from sgcontainernet.net import SGContainernet
from subprocess import Popen, PIPE
from mininet.util import decode
from mininet.node import Controller, RemoteController, OVSHtbQosSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
setLogLevel('info')

def sh(cmd):
    "Send a command to the shell."
    info(cmd + '\n')
    result = Popen(['/bin/sh', '-c', cmd], stdout=PIPE).communicate()[0]
    return decode(result)

def addLinkOnSwitch(node1, node2, ifaces, port1=None, port2=None, 
                    cls=None, **params):
    "Modify net.addLink() with recording interfaces on each switch."
    intfs = net.addLink(node1, node2, port1=port1, port2=port2, cls=cls, **params)
    ifaces.append(intfs.intf1)
    ifaces.append(intfs.intf2)
    return ifaces

def setQos(ifaces):
    for iface in ifaces:
        sh('ovs-vsctl set port %s qos=@newqos -- \
        --id=@newqos create qos type=linux-htb queues=1=@q1,2=@q2,3=@q3,4=@q4 -- \
        --id=@q1 create queue other-config:priority=1 other-config:min-rate=10000 other-config:max-rate=100000 -- \
        --id=@q2 create queue other-config:priority=0 other-config:min-rate=9600 -- \
        --id=@q3 create queue other-config:priority=1 other-config:min-rate=3000000 other-config:max-rate=5000000 -- \
        --id=@q4 create queue other-config:priority=1 other-config:max-rate=1000000' % iface)


if __name__ == '__main__':
    #exec(open("/home/sgsdn/workspace/sflow-rt/extras/sflow.py").read())
    subnet = '10.0.0.0/8'
    net = SGContainernet(controller=RemoteController, ipBase=subnet)

    info('*** Adding controller\n')
    c1 = net.addController('c1', ip='127.0.0.1', port=6633)

    info('*** Adding docker containers\n')
    vpn = net.addSGVPN('vpn', ip='10.0.0.250', mac='00:00:00:00:99:99', subnet=subnet)

    SGHosts = []
    e1 = net.addTPHost('e1', ip='10.0.1.201', mac='00:00:00:00:00:01')
    e2 = net.addTPHost('e2', ip='10.0.1.202', mac='00:00:00:00:00:02')
    e3 = net.addTPHost('e3', ip='10.0.1.203', mac='00:00:00:00:00:03')
    d1 = net.addTPHost('d1', ip='10.0.1.211', mac='00:00:00:00:00:11')
    v1 = net.addTPHost('v1', ip='10.0.1.221', mac='00:00:00:00:00:21')

    e4 = net.addTPHost('e4', ip='10.0.2.204', mac='00:00:00:00:00:04')
    e5 = net.addTPHost('e5', ip='10.0.2.205', mac='00:00:00:00:00:05')
    e6 = net.addTPHost('e6', ip='10.0.2.206', mac='00:00:00:00:00:06')
    d2 = net.addTPHost('d2', ip='10.0.2.212', mac='00:00:00:00:00:12')
    v2 = net.addTPHost('v2', ip='10.0.2.222', mac='00:00:00:00:00:22')

    e7 = net.addTPHost('e7', ip='10.0.3.207', mac='00:00:00:00:00:07')
    e8 = net.addTPHost('e8', ip='10.0.3.208', mac='00:00:00:00:00:08')
    e9 = net.addTPHost('e9', ip='10.0.3.209', mac='00:00:00:00:00:09')
    d3 = net.addTPHost('d3', ip='10.0.3.213', mac='00:00:00:00:00:13')
    v3 = net.addTPHost('v3', ip='10.0.3.223', mac='00:00:00:00:00:23')

    SGHosts += [e1, e2, e3, d1, v1, e4, e5, e6, d2, v2, e7, e8, e9, d3, v3]
    # SGHosts += [e1, e2, e4, e5, e7, e8]

    info('*** Adding switches\n')
    # s1 = net.addSwitch('s1', cls=OVSHtbQosSwitch)
    # s2 = net.addSwitch('s2', cls=OVSHtbQosSwitch)
    # s3 = net.addSwitch('s3', cls=OVSHtbQosSwitch)
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    info('*** Creating links\n')
    net.addLink(s1, vpn)

    net.addLink(s1, e1)
    net.addLink(s1, e2)
    net.addLink(s1, e3)
    net.addLink(s1, d1)
    net.addLink(s1, v1)

    net.addLink(s2, e4)
    net.addLink(s2, e5)
    net.addLink(s2, e6)
    net.addLink(s2, d2)
    net.addLink(s2, v2)

    net.addLink(s3, e7)
    net.addLink(s3, e8)
    net.addLink(s3, e9)
    net.addLink(s3, d3)
    net.addLink(s3, v3)

    ifaces = []
    ifaces = addLinkOnSwitch(s1, s2, ifaces=ifaces)
    ifaces = addLinkOnSwitch(s2, s3, ifaces=ifaces)
    
    # ifaces = addLinkOnSwitch(s1, s2, ifaces=ifaces, cls=TCLink, bw=10)
    # ifaces = addLinkOnSwitch(s2, s3, ifaces=ifaces, cls=TCLink, bw=10)
    
    info('*** Starting network\n')
    net.start()

    for host in SGHosts:
        net.enableNAT(host, '10.0.0.250')

    info('*** Setting QoS strategy on each switch interface\n')
    print(ifaces)
    setQos(ifaces)

    # info('*** Testing connectivity\n')
    #net.ping([e1, e2])
    info('*** Running CLI\n')
    CLI(net)
    info('*** Stopping network')
    net.stop()
