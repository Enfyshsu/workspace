import socket
import sys
import xmpp
import queue
import threading
import select
import time
from sgpacket.abstract import ITransmitterL3

class Client(ITransmitterL3):
    def __init__(self, server_ip = '127.0.0.1', port = 5222):
        self.server_ip = server_ip
        self.port = port
        self.BUFFER_SIZE = 1024
        self.onlineList = []
        self.username = "sgsdn"
        self.pwd = "test"
        self.command_q = queue.Queue()
        self.th = None
         
    def _messageCB(self, sess, mess):
        message = xmpp.protocol.Message(node=mess)
        msgFrom = message.getFrom()
        msgTo = message.getTo()
        msgText = message.getBody()
        print(msgFrom, ">>", msgText)

    def _iqCB(self, sess, mess):
        iq = xmpp.protocol.Iq(node=mess)
        query = iq.getTag("query")
        itens = query.getTags("item")
        self.onlineList = []
        for item in itens:
            onlineList.append(str(item).replace("<item name=\"","").replace("\" />",""))
        print("Online:")
        for item in self.onlineList:
            print("\t" + item)
            
    def _start(self):
        userName = self.username
        pwd = self.pwd
        
        # Connect with the server
        # jid = xmpp.JID(userName)
        connection = xmpp.Client(self.server_ip)
        print("Connecting...")
        connection.connect(server=(self.server_ip, self.port))
        connection.RegisterHandler("message", self._messageCB)
        connection.RegisterHandler("iq", self._iqCB)
        result = connection.auth(userName, pwd, 'test')
        connection.sendInitPresence()
        print("Connected!")

        while True:
            connection.Process(0.15)
            if not self.command_q.empty():
                userTo = self.command_q.get()
                if userTo == ":close":
                    break
                # message = self.command_q.get() + ', time: ' + str(time.time())
                message = self.command_q.get()
                if message.find('time'):
                    message = '<time> ' + str(time.time())
                msg = xmpp.Message(userTo, message)
                connection.send(msg)
        connection.disconnect()
        print("Disconnected.")
        return
        
    def run(self):
        self.th = threading.Thread(target = self._start)
        self.th.start()
        
    def stop(self):
        self.command_q.put(":close")
    
    def join(self):
        self.th.join()
        
    def send_msg(self, to, msg):
        self.command_q.put(to)
        self.command_q.put(msg)
        
    def set_server_ip(self, ip):
        self.server_ip = ip
        
    def set_server_port(self, port):
        self.port = port
    
    def send_one(self):
        self.send_msg('Edward', 'hmmmmmm')