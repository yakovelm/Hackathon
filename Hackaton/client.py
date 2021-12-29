import socket
import struct
import selectors
import sys

teamName=b"SorryException\n"

class Client:
    def __init__(self):
        self.sock = None
        self.sel=selectors.DefaultSelector()

    def start(self):
        print("Client Started, listening for offer requests...")
        self.looking_for_server()


    def looking_for_server(self):
        print("Client::looking_for_server")
        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
        sock.bind(('',13117))
        massage, address=sock.recvfrom(1024) # need to be 7
        self.check_package(massage,address)


    def check_package(self,message,address):
        print("Client::check_package")

        pre,type,port=struct.unpack("!IBH",message)

        if pre==0xabcddcba and type==0x02:
            self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            print((address[0],port))
            self.sock.connect((address[0],port))
            print("nitay")
            self.sock.send(teamName)
            self.game_mode()
            
            


        else:
            print("Error")



    def game_mode(self):
        print("Client::game_mode")
        inChar=""
        self.sel.register(fileobj=sys.stdin, events=selectors.EVENT_READ)
        self.sock_tcp.setblocking(False)
        self.sel.register(self.sock,events=selectors.EVENT_READ)
        question=self.sock.recv(1024)
        print(question)
        


if __name__ == '__main__':
    Client().start()
