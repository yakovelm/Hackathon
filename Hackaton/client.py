import socket
import struct


class Client:

    def start(self):
        print("Client Started, listening for offer requests...")
        self.looking_for_server()


    def looking_for_server(self):
        print("Client::looking_for_server")
        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock.bind(('',13117))
        massage, address=sock.recvfrom(1024) # need to be 7
        self.check_package(massage,address)


    def check_package(self,message,address):
        print("Client::check_package")
        pre=struct.unpack("L",message[0:4])[0]
        type=struct.unpack("B",message[4:5])[0]

        if pre==0xabcddcba and type==0x02:
            port=struct.unpack("H",message[5:7])[0]
            print(port)
            sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.connect((address[0],port))
            sock.sendall(b"this is sendall")
            print("here i send")


        else:
            print("aleks")







    def connection_with_server(self):
        pass


    def game_mode(self):
        pass

