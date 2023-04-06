import socket
import threading
import xmpp
import time
import statistics
from sgpacket.abstract import IReceiver

class Server(IReceiver):
    def __init__(self, host = '0.0.0.0', port = 5222):
        self.ID = 4235063100
        self.BUFFER_SIZE = 1024
        self.host = host
        self.port = port
        self.onlineList = []
        self.msgList = {}
        self.conn = None
        self.s = None
    
    def _handler(self, client_conn, client_addr):
        # Ref: https://github.com/alissonmbr/xmpp
        print("Connected with ", client_addr)

        # Client request: create stream
        
        data = client_conn.recv(self.BUFFER_SIZE)
        
        print("Message from client: ", data)
        
        # Server response: stream ID and available features
        resStream = "<?xml version=\'1.0\'?>" 
        resStream += "<stream:stream xmlns=\'jabber:client\' xmlns:stream=\'http://etherx.jabber.org/streams\'"
        resStream += " id=\'" + str(self.ID) + "\' from=\'" + str(self.host) + "\' version=\'1.0\' xml:lang=\'en\'>"
        self.ID += 1
        resStream += "<stream:features>"
        resStream += "<compression xmlns=\"http://jabber.org/features/compress\">"
        resStream += "<method>zlib</method>"
        resStream += "</compression>"
        resStream += "<auth xmlns=\'http://jabber.org/features/iq-auth\'/>"
        resStream += "</stream:features>"	
        client_conn.send(resStream.encode('utf-8'))
        
        # Client request: Authentication Fields
        data = client_conn.recv(self.BUFFER_SIZE)
        iq = xmpp.protocol.Iq(node=data)
        iqId = iq.getID()
        iqUser = iq.getCDATA()
        self.msgList[iqUser] = []
        
        # Server response: Authentication Fields
        resIq = "<iq id=\'" + str(iqId) + "\' type=\'result\'><query xmlns=\'jabber:iq:auth\'><username/><password/><digest/><resource/></query></iq>"
        client_conn.send(resIq.encode('utf-8'))
        
        # Client response: Authentication information
        data = client_conn.recv(self.BUFFER_SIZE)
        iq = xmpp.protocol.Iq(node=data)
        iqId = iq.getID()
        userDigest = iq.getCDATA()
        userDigest = userDigest.replace(iqUser,"")
        userDigest = userDigest.replace("botty","")
        self.onlineList.append(iqUser)
        print("User:", iqUser)
        print("Digest:", userDigest)
        
        # Server response: Authentication status
        authResponse = "<iq type=\'result\' id=\'" + str(iqId) + "'/>"
        client_conn.send(authResponse.encode('utf-8'))
        
        # Client: Presence
        data = client_conn.recv(self.BUFFER_SIZE)	
        queryItens = ""
        for x in self.onlineList:
            queryItens += "<item name=\"" + x + "\"/>"
        onlineStatus = xmpp.protocol.Iq(node="<iq> <query xmlns=\"http://jabber.org/protocol/disco#items\" node=\"online users\" >" + queryItens + "</query> </iq>")
        # client_conn.send(onlineStatus.encode('utf-8'))
        
        while True:
            data = client_conn.recv(self.BUFFER_SIZE)
            # Disconnect
            if data == b"</stream:stream>":
                self.onlineList.remove(iqUser)
                client_conn.send(b"</stream:stream>")
                break
            
            # Refresh online list
            queryItens = ""
            for x in self.onlineList:
                queryItens += "<item name=\"" + x + "\"/>"
            onlineStatus = xmpp.protocol.Iq(node="<iq> <query xmlns=\"http://jabber.org/protocol/disco#items\" node=\"online users\" >" + queryItens + "</query> </iq>")
            
            # Receive a message from the client
            if data.find("<message".encode('utf-8')) >= 0 :
                msgP = xmpp.protocol.Message(node=data)
                msgTo = msgP.getTo()
                msgText = msgP.getBody()
                if str(msgTo) in self.onlineList:
                    if len(self.msgList[str(msgTo)]) > 0: 
                        self.msgList[msgTo].insert(0,msgP)
                    else:
                        self.msgList[str(msgTo)].append(msgP)		
                
            # Send all message to the client
            while len(self.msgList[iqUser]) > 0:
                string1 = str(self.msgList[iqUser].pop())
                client_conn.send(string1.encode('utf-8'))
        self.s.close()
        print("Connetion with ", client_addr, " is closed.")
        
    def _start(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host, self.port))
        self.s.listen(5)
        print('Waiting for connection')
        self.conn, addr = self.s.accept()
        self._handler(self.conn, addr)
        
    def run(self):
        self.th = threading.Thread(target=self._start)
        self.th.start()
        
    def stop(self):
        self.s.close()
            
    def set_ip(self, ip):
        self.host = ip
        
    def set_port(self, port):
        self.port = port