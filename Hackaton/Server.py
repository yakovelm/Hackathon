import socket



def tester():
    sock= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(str.encode("1"),("127.0.0.1",13117))


if __name__ == '__main__':
    tester()