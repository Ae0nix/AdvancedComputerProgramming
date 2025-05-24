import grpc
import proto.OrderManagment_pb2 as om_pb2
import proto.OrderManagment_pb2_grpc as om_pb2_grpc

import multiprocessing as mp
import sys
import random

ITEMS = ["Item A", "Item B", "Item C", "Item D", "Item E", "Item F", "Item G", "Item H"]
DESTINATIONS = ["San Jose, CA", 'San Francisco, CA', 'Mountain View, CA', 'San Diego, CA']

def main():

    channel = grpc.insecure_channel('localhost:' + sys.argv[1])
    stub = om_pb2_grpc.OrderManagmentStub(channel)

    for _ in range(5):
        ord = om_pb2.Order(
            id="", price=random.randint(500, 4000),
            itemList=[ITEMS[random.randint(0, 7)], ITEMS[random.randint(0, 7)]],
            description="Updated desc",
            destination=DESTINATIONS[random.randint(0,3)]
        )
        id = stub.addOrder(ord)
        print("[client] The ID given to order is: " + id.value)
        
        print("[client] Verify the order valeues are right: ")
        enteredOrder = stub.getOrder(id)
        print("- id: " + enteredOrder.id)
        print("- Item in Order:")
        for order in enteredOrder.itemList:
            print(f"\t - {order}")
        print("- description: " + enteredOrder.description)
        print("- price: " + str(enteredOrder.price))
        print("- destination: " + enteredOrder.destination)

    #item to search
    itemToSearch = ITEMS[random.randint(0, 7)]
    print("[client] Search for: " + itemToSearch)
    
    listOfOrderContainingTheItems = list()
    for order in stub.searchOrders(om_pb2.StringMessage(value=itemToSearch)):
        # print("The following order contais the item searched: " + order.id)
        listOfOrderContainingTheItems.append(order.id)
    
    print("The following order contais the item searched: " + str(listOfOrderContainingTheItems))
    

    print("[client] Generating four orders to ship...")
    print("[client] Printing info about shipments")
    for shipment in stub.processOrders(generate_orders_to_ship()):
        print("- Shipment ID: " + shipment.id)
        print("- Shipment state: " + shipment.state)
        print("- Shipment of the following orders:")
        for order in shipment.orderList:
            print(f"\t - {order.id}")

def generate_orders_to_ship():
    print("Generating five orders")

    ord0 = om_pb2.Order(
        id='104', price=2332,
        itemList=['Item - A', 'Item - B'],  
        description='Updated desc', 
        destination='San Jose, CA'
    )
    
    ord1 = om_pb2.Order(
        id='105', price=3500,
        itemList=['Item - A', 'Item - B'],  
        description='Updated desc', 
        destination='San Francisco, CA'
    )
    
    ord2 = om_pb2.Order(
        id='106', price=1500,
        itemList=['Item - A', 'Item - C'],  
        description='Updated desc', 
        destination='San Francisco, CA'
    )
    
    ord3 = om_pb2.Order(
        id='107', price=800,
        itemList=['Item - A', 'Item - A'],  
        description='Updated desc', 
        destination='Mountain View, CA'
    )

    list = [ord0, ord1, ord2, ord3]
    for order in list:
        yield order


if __name__ == "__main__":
    main()


    