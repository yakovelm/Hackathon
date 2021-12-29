import ipaddress
import random
import select
import selectors
import socket
import struct
import threading
import time


class Server:
    
    def __init__(self):
        self.name="the Server connect with you\n what is your name?"
        self.sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_tcp.setblocking(True)
        self.sock_tcp.bind(('192.168.56.1', 13118))
        self.port=13118
        self.player1_socket=None
        self.player2_socket=None
        self.players=0
        self.solution=None


    def create_math(self):
        sign=random.choice(["+","-"])
        digits=[1,2,3,4,5,6,7,8,9]
        num1 = random.choice(digits)
        num2 = random.choice(digits)
        if sign=="+":
            while num1+num2>=10:
                num2=random.choice(digits)
            self.solution=num1+num2
        else:
            while num1+num2<0:
                num2=random.choice(digits)
            self.solution = num1 - num2
        return "How much is "+str(num1)+sign+str(num2)+"?"




    def start_game(self):
        name1=self.player1_socket.recv(1024)
        name2=self.player2_socket.recv(1024)
        message="Welcome to Quick Maths: \nPlayer 1: "+ name1 +"\nPlayer 2 : " +name2+"\n==\n Please answer the following question as fast as you can:\n"
        formula=self.create_math()
        formula_in_bytes=formula.encode()
        dec=message.encode()
        self.player1_socket.sendto(dec)
        self.player2_socket.sendto(dec)
        sel=selectors.DefaultSelector()
        #t1=threading.Thread(()-> self.player1_socket.sendto(formula_in_bytes))
        #t2 = threading.Thread(()-> self.player2_socket.sendto(formula_in_bytes))
        self.player1_socket
        reads,_,_=select.select([self.player1_socket,self.player2_socket],[],[],10)
        time.sleep(10)
        t1.start()
        t2.start()
        if len(reads)==0:
            #draw
        elif reads[1].
        self.player1_socket.sendto(formula_in_bytes)
        self.player2_socket.sendto(formula_in_bytes)


        t1=threading.Thread(target=self.solve, args=(self.player2_socket,message,formula))
        t2=threading.Thread(target=self.solve, args=(self.player2_socket,message,formula))

    def solve(self,player,formula):
        player.sendto(formula)



    def init_Broad_Cast(self):
        try:
            broad_cast = ("255.255.255.255", 13117)
            pre = struct.pack("L", 0xabcddcba)
            offer = struct.pack("B", 0x2)
            port = struct.pack("H", self.port)
            massage = b''.join([pre, offer, port])

            while self.players<2:
                self.sock_udp.sendto(massage, broad_cast)
                time.sleep(1)
        except Exception as e:
            print(e)

    def init_accept_thread(self):
        while self.players<2:
            self.sock_tcp.listen(2)
            new_conn,address=self.sock_tcp.accept()
            with new_conn:
                if self.players==0:
                    self.player1_socket=new_conn
                else:
                    self.player2_socket=new_conn
                    self.start_game()

    def run(self):
        self.init_server()
        threading.Thread(self.init_Broad_Cast()).start()
        threading.Thread(self.init_accept_thread()).start()



if __name__ == '__main__':
    Server().run()

