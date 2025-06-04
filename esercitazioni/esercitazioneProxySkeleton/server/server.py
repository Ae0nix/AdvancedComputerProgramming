from serverImpl import MagazzinoImpl
from serverSkeleton import ServerSkeleton

IP = "localhost"
PORT = 0
QUEUE_SIZE = 5

if __name__ == "__main__":
    
    impl = MagazzinoImpl(QUEUE_SIZE)
    serverSkeleton = ServerSkeleton(IP, PORT, impl)
    serverSkeleton.run_skeleton()