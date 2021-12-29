import ipaddress
import random
from select import select

import socket
import struct
from threading import Thread
import time


class Server:

    def __init__(self):
        self.name = "the Server connect with you\n what is your name?"
        self.sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_tcp.bind(('', 2119))
        self.port = 2119
        self.player1_socket = None
        self.player2_socket = None
        self.players = 0
        self.solution = None

    def create_math(self):
        sign = random.choice(["+", "-"])
        digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        num1 = random.choice(digits)
        num2 = random.choice(digits)
        if sign == "+":
            while num1 + num2 >= 10:
                num2 = random.choice(digits)
            self.solution = num1 + num2
        else:
            while num1 + num2 < 0:
                num2 = random.choice(digits)
            self.solution = num1 - num2
        return "How much is " + str(num1) + sign + str(num2) + "?"

    def start_game(self):
        try:
            name1 = self.player1_socket.recv(1024).decode()
            name2 = self.player2_socket.recv(1024).decode()
            message = "Welcome to Quick Maths: \nPlayer 1: " + name1 + "\nPlayer 2 : " + name2 + "\n==\n Please answer the following question as fast as you can:\n"
            message =message+ self.create_math()
            formula_in_bytes = message.encode()

            time.sleep(10)
            self.player1_socket.send(formula_in_bytes)
            self.player2_socket.send(formula_in_bytes)

            yaki, _, _ = select([self.player1_socket, self.player2_socket], [], [], 10)
            if len(yaki) == 0:
                write = "is draw! the right answer is" + str(self.solution)
                self.player1_socket.send(write.encode())
                self.player2_socket.send(write.encode())
            else:
                if yaki[0] == self.player1_socket:
                    ans = self.player1_socket.recv(1024).decode()
                    if str(self.solution) == ans:
                        write = ("the winner is " + name1 + ", the loser is " + name2+"\n the right answer is "+str(self.solution)).encode()
                        self.player1_socket.send(write)
                        self.player2_socket.send(write)
                    else:
                        write = ("the winner is " + name2 + ", the loser is " + name1+"\n the right answer is "+str(self.solution)).encode()
                        self.player1_socket.send(write)
                        self.player2_socket.send(write)
                else:
                    ans = self.player2_socket.recv(1024).decode()
                    if str(self.solution) == ans:
                        write = "the winner is " + name2 + ", the loser is " + name1+"\n the right answer is "+str(self.solution)
                        self.player1_socket.send(write.encode())
                        self.player2_socket.send(write.encode())
                    else:
                        write = "the winner is " + name1 + ", the loser is " + name2+"\n the right answer is "+str(self.solution)
                        self.player1_socket.send(write.encode())
                        self.player2_socket.send(write.encode())
            self.players=0
        except Exception as e:
            print(e)

    def init_Broad_Cast(self):
        try:
            broad_cast = ("<broadcast>", 13117)
            massage=struct.pack("!IBH",0xabcddcba,0x2,self.port)

            while self.players < 2:
                self.sock_udp.sendto(massage, broad_cast)
                time.sleep(1)
        except Exception as e:
            print(e)

    def init_accept_thread(self):
        while self.players < 2:
            self.sock_tcp.listen(2)
            new_conn, address = self.sock_tcp.accept()
            if self.players == 0:
                self.player1_socket = new_conn
                self.players=1
            else:
                self.player2_socket = new_conn
                self.players=2

    def run(self):
        while True:
            t1 = Thread(target=self.init_Broad_Cast)
            t2 = Thread(target=self.init_accept_thread)
            t1.start()
            t2.start()
            t1.join()
            t2.join()
            self.start_game()


if __name__ == '__main__':
    Server().run()
