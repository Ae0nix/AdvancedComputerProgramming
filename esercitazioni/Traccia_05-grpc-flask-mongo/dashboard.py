import Statistics_pb2 as s_pb2
import Statistics_pb2_grpc as s_pb2_grpc

import grpc

def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = s_pb2_grpc.statisticStub(channel)

    print('[DASHBORAD] Sending request for availabe sensors')
    response = stub.getSensors(s_pb2.Empty())

    sensors = []

    for sensor in response:
        print(f"[DASHBOARD] Received sensor with id: {sensor.id} of type {sensor.data_type}")
        sensors.append(sensor)


    # print(f"[CLIENT] The mean value of the measurements made by the sensor with id: {sensor["id"]} is {mean.value}")
    for sensor in sensors:
        
        mean = stub.getMean(s_pb2.MeanRequest(sensor_id=sensor.id, data_type=sensor.data_type))
        print(f"[DASHBOARD] Requested mean for sensor: {sensor.id}-{sensor.data_type}")
        print(f"\t [DASHBOARD] Mean for sensor[{sensor.id}]: {mean.value}")



if __name__ == "__main__":
    run()

    