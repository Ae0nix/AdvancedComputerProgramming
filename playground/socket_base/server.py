import socket
import threading
import time

def reverse_function(conn):
    with conn:
        data = conn.recv(1024)
        reversedData = data[::-1]
        time.sleep(5)
        conn.send(reversedData)

PORT = 0 #in modo tale che il sistema operativo attribuisca il primo porto libero
IP = "127.0.0.1"

s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
s.bind((IP, PORT))
print("[server] in ascolto su porto: " + str(s.getsockname()[1]))

s.listen()

print("[server] in attesa di connessioni...")
while True:
    conn, addr = s.accept() #ricordiamo che la socket "s" serve "solo" per l'ascolto delle connessioni, la gestione la fa conn
    th1 = threading.Thread(target=reverse_function, args=(conn, ))
    th1.start()
    th1.join()

s.close()
