# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet, ipv4, tcp, udp
from ryu.lib.packet import ether_types
from ryu.lib.packet import in_proto
from ryu.topology import event

PORT_XMPP = 5222
PORT_DNP3 = 20000
PORT_UDP = 7001

class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src
        dst_ip = ''
        src_ip = ''

        dpid = format(datapath.id, "d").zfill(16)
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        priority = 1
        match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
        actions = [parser.OFPActionSetQueue(4), parser.OFPActionOutput(out_port)]

        if eth.ethertype == ether_types.ETH_TYPE_IP:
            # insert flow rule for xmpp, dnp3, and udp
            ip = pkt.get_protocol(ipv4.ipv4)
            src_ip = ip.src
            dst_ip = ip.dst

            t = pkt.get_protocol(tcp.tcp)
            u = pkt.get_protocol(udp.udp)
            
            # the priority is higher than forwarding the pkt to controller (priority = 2)
            
            # insert flow rule for xmpp (tcp port 5222)
            if t is not None and t.dst_port == PORT_XMPP:
                protocol = in_proto.IPPROTO_TCP
                dst_port = PORT_XMPP
                priority = 10
                match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ip_proto=protocol, ipv4_src=src_ip, ipv4_dst=dst_ip, tcp_dst=dst_port)
                actions = [parser.OFPActionSetQueue(1), parser.OFPActionOutput(out_port)]
            
            # insert flow rule for dnp3 (tcp or udp port 20000)
            elif t is not None and t.dst_port == PORT_DNP3:
                protocol = in_proto.IPPROTO_TCP
                dst_port = PORT_DNP3
                priority = 10
                match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ip_proto=protocol, ipv4_src=src_ip, ipv4_dst=dst_ip, tcp_dst=dst_port)
                actions = [parser.OFPActionSetQueue(2), parser.OFPActionOutput(out_port)]
            
            elif u is not None and u.dst_port == PORT_DNP3:
                protocol = in_proto.IPPROTO_UDP
                dst_port = PORT_DNP3
                priority = 10
                match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ip_proto=protocol, ipv4_src=src_ip, ipv4_dst=dst_ip, udp_dst=dst_port)
                actions = [parser.OFPActionSetQueue(2), parser.OFPActionOutput(out_port)]
            
            # insert flow rule for video stream (udp port 7001 for example)
            elif u is not None and u.dst_port == PORT_UDP:
                protocol = in_proto.IPPROTO_UDP
                dst_port = PORT_UDP
                priority = 10
                match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ip_proto=protocol, ipv4_src=src_ip, ipv4_dst=dst_ip, udp_dst=dst_port)
                actions = [parser.OFPActionSetQueue(3), parser.OFPActionOutput(out_port)]
            
            # self.add_flow(datapath, priority, match, actions)

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            self.add_flow(datapath, priority, match, actions)

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)

    @set_ev_cls(event.EventSwitchEnter)
    def switch_enter_handler(self, ev):
        # When a switch enters the controller,
        # add rules to forward the xmpp, dnp3, and udp
        # packets to the controller to find out_ports.

        datapath = ev.switch.dp
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        priority = 2

        # insert flow rule for xmpp (tcp port 5222)
        protocol = in_proto.IPPROTO_TCP
        dst_port = PORT_XMPP
        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ip_proto=protocol, tcp_dst=dst_port)
        actions = [parser.OFPActionSetQueue(1), parser.OFPActionOutput(ofproto.OFPP_CONTROLLER)]
        self.add_flow(datapath, priority, match, actions)

        # insert flow rule for dnp3 (tcp or udp port 20000)
        protocol = in_proto.IPPROTO_TCP
        dst_port = PORT_DNP3
        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ip_proto=protocol, tcp_dst=dst_port)
        actions = [parser.OFPActionSetQueue(2), parser.OFPActionOutput(ofproto.OFPP_CONTROLLER)]
        self.add_flow(datapath, priority, match, actions)

        protocol = in_proto.IPPROTO_UDP
        dst_port = PORT_DNP3
        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ip_proto=protocol, udp_dst=dst_port)
        actions = [parser.OFPActionSetQueue(2), parser.OFPActionOutput(ofproto.OFPP_CONTROLLER)]
        self.add_flow(datapath, priority, match, actions)

        # insert flow rule for video stream (udp port 7001 for example)
        protocol = in_proto.IPPROTO_UDP
        dst_port = PORT_UDP
        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ip_proto=protocol, udp_dst=dst_port)
        actions = [parser.OFPActionSetQueue(3), parser.OFPActionOutput(ofproto.OFPP_CONTROLLER)]
        self.add_flow(datapath, priority, match, actions)
