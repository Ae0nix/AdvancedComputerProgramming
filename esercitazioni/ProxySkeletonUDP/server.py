from serverImpl import serverImpl
from serverSkeleton import ServerSkeleton

HOST = "localhost"
PORT = 0

if __name__ == "__main__":

    impl = serverImpl()

    skeleton = ServerSkeleton(HOST, PORT, impl)

    skeleton.run()