import socket


class Client:

    def start(self):
        print("Client Started, listening for offer requests...")
        self.looking_for_server()


    def looking_for_server(self):
        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.bind(('',13117))
        massage, address=sock.recvfrom(1024) # need to be 7
        print(massage,address)







    def connection_with_server(self):
        pass


    def game_mode(self):
        pass

