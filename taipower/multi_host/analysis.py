import numpy as np
import matplotlib.pyplot as plt
import os

path_prefix = os.path.expanduser( '~' ) + '/workspace/taipower/part1/sgpacket/log/'

xmpp_data = np.load(path_prefix + 'XMPP_1680701232.npy')
latency = np.array(xmpp_data)[150:, 1] * 1000
mean = np.mean(latency)
std = np.std(latency)
print("XMPP Mean: %.3f ms" %mean) 
print("XMPP Standard Deviation: %.3f ms" % std)

dnp3_data = np.load(path_prefix + 'DNP3_1680701232.npy')
latency = np.array(dnp3_data)[150:, 1] * 1000
mean = np.mean(latency)
std = np.std(latency)
print("DNP3 Mean: %.3f ms" %mean) 
print("DNP3 Standard Deviation: %.3f ms" % std)

udp_data = np.load(path_prefix + 'UDP_1680701232.npy')
latency = np.array(udp_data)[150:, 1] * 1000
mean = np.mean(latency)
std = np.std(latency)
print("UDP Mean: %.3f ms" %mean) 
print("UDP Standard Deviation: %.3f ms" % std)