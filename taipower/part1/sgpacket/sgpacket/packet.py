from enum import Enum

class PacketType(Enum):
    TCP = 0
    UDP = 1
    DNP3 = 2
    MMS = 3
    XMPP = 4
    GOOSE = 5
    SV = 6