from select import select
import socket
import struct
import selectors
import sys

teamName="SorryException"

class Client:
    def __init__(self):
        self.sock = None

    def start(self):
        print("Client Started, listening for offer requests...")
        while True:
            self.looking_for_server()


    def looking_for_server(self):

        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
        sock.bind(('',13117))
        massage, address=sock.recvfrom(1024) # need to be 7
        self.check_package(massage,address)


    def check_package(self,message,address):

        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        pre,type,port=struct.unpack("!IBH",message)

        if pre==0xabcddcba and type==0x02:

            self.sock.connect((address[0],port))
            self.sock.send(teamName.encode())
            self.game_mode()
            
            


        else:
            print("Error")



    def game_mode(self):
        try:
            print(self.sock.recv(1024).decode())
            check,_,_=select([sys.stdin,self.sock],[],[],10)
            if len(check)==1 and check[0]==sys.stdin:
                answer=sys.stdin.read(1)
                self.sock.send(answer.encode())
            
            p=self.sock.recv(1024).decode()
            print(p)
        except Exception as e:
            print(e)

        


if __name__ == '__main__':
    Client().start()
