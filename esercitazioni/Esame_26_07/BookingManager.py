import requests
import stomp
import time

BASE_URL = "http://localhost:5001"


class MyListener(stomp.ConnectionListener):

    def __init__(self, conn):
        self.conn = conn

    def on_message(self, frame):
        message_type = frame.body.split("-")[0]

        match message_type:
            case "CREATE":
                client = frame.body.split("-")[1]
                hotel = frame.body.split("-")[2]
                operator = frame.body.split("-")[3]
                nights = frame.body.split("-")[4]
                people = frame.body.split("-")[5]
                cost = frame.body.split("-")[6]

                message = {
                    "client": client,
                    "hotel": hotel,
                    "operator":operator,
                    "nights": nights,
                    "people": people,
                    "cost": cost
                }

                try:
                    response = requests.put(url=BASE_URL+"/create_booking", json=message)
                    response.raise_for_status()
                    print(f"[BOOKING MANAGER] Sent CREATE request correctly to database. status code: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print("[BOOKING MANAGER] Error while sending the CREATE request")
                else:
                    conn.send(body="ACK", destination="/topic/response")

            case "UPDATE":
                operator = frame.body.split("-")[1]
                nights = frame.body.split("-")[2]
                discount = frame.body.split("-")[3]

                message = {
                    "operator": operator,
                    "nights": nights,
                    "discount": discount
                }

                try:
                    response = requests.post(url=BASE_URL+"/update_booking", json=message)
                    response.raise_for_status()
                    print(f"[BOOKING MANAGER] Sent UPDATE request correctly to database. status code: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print("[BOOKING MANAGER] Error while sending the UPDATE request")
                else:
                    conn.send(body="ACK", destination="/topic/response")
                


if __name__ == "__main__":
    conn = stomp.Connection([("127.0.0.1", 61613)])
    conn.set_listener('', MyListener(conn))
    conn.connect(wait=True)
    conn.subscribe(destination="/topic/request", id=1, ack="auto")

    while True:
        time.sleep(60)

    conn.disconnect()
