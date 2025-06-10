POSSIBLE_METHOD=["setCount", "sum", "increment"]

def serverThread(skeleton, conn):
    message = conn.recv(1024).decode("utf-8")

    print(f"[SKELETON] Message received {message}")
    requestType = message.split("-")[0]
    print(f"[DEBUG] request type {requestType} !!!!!!!!!!!!!!")
    match requestType:
        case "setCount":
            id = message.split("-")[1]
            valueToSet = message.split("-")[2]
            result = skeleton.setCount(id, valueToSet)

        case "sum":
            valueToSum = message.split("-")[1]
            result = skeleton.sum(valueToSum)

        case "increment":
            result = skeleton.increment()


    conn.send(str(result).encode("utf-8"))
