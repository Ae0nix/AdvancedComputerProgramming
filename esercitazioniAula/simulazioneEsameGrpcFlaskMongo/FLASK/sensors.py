import threading as mt
import random
import requests

supported_types = ["temp", "press"]
SERVER_URL = "http://localhost:5001"

def thread_func(sensor_id):
    data_type = supported_types[random.randint(0,1)]

    #devo fare una richiesta del tipo request.post(qualcosa)

    """
    1. specifico il body della post /sensor in formato JSON
    """

    sensor_spec = {
        "__id": sensor_id,
        "data_type": data_type
    }

    response = requests.post(SERVER_URL + "/sensor", json=sensor_spec)
    try:
        response.race_for_status()
    except requests.exceptions.HTTPError:
        print("[CLIENT] errore ricevuto " + response.status_code + "response_body " + response.text)
    else:
        print("[CLIENT] sensor_id " + sensor_id + "sensor_spec" + sensor_spec)

    ### Genero il dato da mandare
    for _ in range(5):
        data = {
            "sensor_id": sensor_id,
            "data": random.randint(1,50)
        }

        response = requests.post(SERVER_URL + "/data/" + data_type, json=data)
        try:
            response.race_for_status()
        except requests.exceptions.HTTPError:
            print("[CLIENT] errore ricevuto " + response.status_code + "response_body " + response.text)
        else:
            print("[CLIENT] sensor_id " + sensor_id + "data" + data)
        

if __name__ == "__main__":

    threads = []

    ###genero e avvio i thread
    for i in range(1,6):
        thd = mt.Thread(target=thread_func, args=(i, ))
        thd.start()

        threads.append(thd)
    
    for thread in threads:
        thread.join()