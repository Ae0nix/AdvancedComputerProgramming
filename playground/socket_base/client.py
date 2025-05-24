import socket
import sys
import argparse


IP = "localhost" 

s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
s.bind((IP, 0))
print("[client] client su porto: " + str(s.getsockname()[1]))

#gestione degli input da terminale
parser = argparse.ArgumentParser()
parser.add_argument("porto_server")
parser.add_argument("stringa")
args = parser.parse_args()

data = args.stringa
s.connect((IP, int(args.porto_server)))


s.send(data.encode("utf-8"))
print("[client] data sent")


response = s.recv(1024)
print("[client] response received "+ response.decode("utf-8"))
