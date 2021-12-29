import ipaddress
import random
import socket
import struct
import threading
import time


class Server:
    
    def __init__(self):
        self.name="the Server connect with you\n what is your name?"
        self.sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_tcp.setblocking(True)
        self.sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.player1_socket=None
        self.player2_socket=None
        self.player1_Name = None
        self.player2_Name = None
        self.math=None
        Self.solution=None

    def init_server(self):
        print("Server::init")
        try:
            print("Server started, listening on IP address:")  # ip
            self.sock_udp.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            self.sock_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.sock_tcp.bind(('192.168.56.1', 13118))
            t = threading.Thread(target=self.my_accept, args=())
            t.start()
            self.udp_work()
        except Exception as e:
            print(e)

    def udp_work(self):
        print("Server::udp_work")
        try:
            port = self.sock_tcp.getsockname()[1]
            broad_cast = ("255.255.255.255", 13117)
            pre = struct.pack("L", 0xabcddcba)
            offer = struct.pack("B", 0x2)
            port = struct.pack("H", port)
            massage = b''.join([pre, offer, port])

            while True:
                self.sock_udp.sendto(massage, broad_cast)
                time.sleep(1)
        except Exception as e:
            print(e)


    def my_accept(self):
        print("Server::my accept")
        while True:
            self.sock_tcp.listen()
            new_conn,address=self.sock_tcp.accept()
            with new_conn:
                if not self.player1_socket is None:
                    threading.Thread(target=self.player_controller, args=(new_conn,True)).start()
                else:
                    threading.Thread(target=self.player_controller, args=(new_conn, False)).start()
                    time.sleep(10)
                    self.start_game()

                #need to wait for 2nd player
    def create_math(self):
        sign=random.choice(["+","-"])
        digits=[1,2,3,4,5,6,7,8,9]
        if sign=="+":
            num1=random.choice([1,2,3,4,5,6,7,8,9,0])
            num2=random.choice()



    def start_game(self):
        message="Welcome to Quick Maths: \nPlayer 1: "+ self.player1_Name +"\nPlayer 2 : " +self.player2_Name+"\n==\n Please answer the following question as fast as you can:\n"
        self.create_math()
        t1=threading.Thread(target=self.solve, args=(self.player2_socket,message))
        t2=threading.Thread(target=self.solve, args=(self.player2_socket,message))



    def player_controller(self,conn,first):
        if first:
            self.player1_socket=conn
            self.player1_Name=conn.recv(1024)
        else:
            self.player2_socket=conn
            self.player2_Name = conn.recv(1024)






if __name__ == '__main__':
    Server().start_game()

