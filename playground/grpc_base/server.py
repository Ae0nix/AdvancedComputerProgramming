from concurrent import futures

import grpc
import hello_pb2
import hello_pb2_grpc

class Greeter(hello_pb2_grpc.GreeterServiceServicer):

    def SayHello(self, request, context):
        return hello_pb2.HelloReply(message="Hello, %s!" % request.value)

def serve():
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    hello_pb2_grpc.add_GreeterServiceServicer_to_server(Greeter(), server)
    port = server.add_insecure_port("0.0.0.0:0")

    server.start()

    print("Server started listening on port " + str(port))

    server.wait_for_termination()
    


if __name__ == "__main__":
    serve()