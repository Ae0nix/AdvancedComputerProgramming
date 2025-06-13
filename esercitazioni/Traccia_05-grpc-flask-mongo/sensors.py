import requests
import random
import threading as mt

NUM_THREAD = 5
SENSOR_TYPE = ["temp", "press"]
BASE_URL = "http://127.0.0.1:5001"
NUM_MEASURE = 5

def thread_func(id, data_type):
    
    registration_request = {
        "_id": id,
        "data_type":data_type
    }

    response = requests.post(url=BASE_URL + "/sensor", json=registration_request)

    #Questo serve per controllare se la richiesta non è andata a buon fine
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print(f"[SENSOR-{id}] Error: Received {response.status_code} - {response.text}")
    else:
        print(f"[SENSORS] Registered a sensor of {data_type} with id: {id}")




    for i in range(NUM_MEASURE):
        measured_data = {
            "sensor_id": id,
            "data": random.randint(1,50)
        }    
    
        response = requests.post(url=BASE_URL + "/data" + f"/{data_type}", json=measured_data)
        
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            print(f"[SENSOR-{id}] Error: Received {response.status_code} - {response.text}")
        else:
            print(f"[SENSORS] Added {data_type} measure with data: {measured_data["data"]}")


if __name__ == "__main__":
    
    threads = []
    for i in range(NUM_THREAD):
        id = i+1
        data_type = SENSOR_TYPE[random.randint(0,1)]
        th = mt.Thread(target=thread_func, args=(id, data_type))
        threads.append(th)
        th.start()


    for thread in threads:
        thread.join()