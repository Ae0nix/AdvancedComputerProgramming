from ServerImpl import ServerImpl

if __name__ == "__main__":
    server = ServerImpl("localhost", 0)
    server.run_func()

    print("[SERVER] ✅ Server started")