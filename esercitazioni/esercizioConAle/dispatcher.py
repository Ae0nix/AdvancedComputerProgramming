import sys

from dispatcherImpl import dispatcherImpl
from dispatcher_skeleton import DispatcherSkeleton

def main():
    
    try:
        HOST = sys.argv[1]
        PORT = sys.argv[2]
    except IndexError:
        print("Please, specify HOST and/or PORT args")
        sys.exit(-1)


dispatcherImpl = dispatcherImpl()
DispatcherSkeleton = DispatcherSkeleton(HOST, int(PORT), dispatcherImpl)
DispatcherSkeleton.runSkeleton()

if __name__ == "__main__":
    main()