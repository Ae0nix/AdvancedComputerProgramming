import grpc
import sys
import hello_pb2
import hello_pb2_grpc

def run():
    with grpc.insecure_channel("localhost:" + sys.argv[1]) as channel:
        stub = hello_pb2_grpc.GreeterServiceStub(channel)

        response = stub.SayHello(hello_pb2.HelloRequest(value="Gianmarco"))
        print("[CLIENT] SayHello invoked Greeter client received: " + response.value)




if __name__== "__main__":
    run()