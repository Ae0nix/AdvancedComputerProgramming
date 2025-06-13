from pymongo import MongoClient
from pymongo.errors import PyMongoError
import grpc
import Statistics_pb2 as s_pb2
import Statistics_pb2_grpc as s_pb2_grpc
import sys
from concurrent import futures

def getDatabase():
    client = MongoClient("mongodb://localhost:27017")
    return client["test_database"]

class StatisticsServicer(s_pb2_grpc.statisticServicer):

    def __init__(self):
        self.db = getDatabase()
        
    def getSensors(self, request, context):
        sensor_collection = self.db["sensors"]

        try:
            sensors = sensor_collection.find({})
        except PyMongoError as e:
            print(f"An error occurred: {e}")
        else:
            for sensor in sensors:
                print(f"[GET SENSORS] Sending sensor: {str(sensor)}")
                yield s_pb2.Sensor(id=str(sensor["_id"]), data_type=sensor["data_type"])

    def getMean(self, request, context):
        sensor_id = request.sensor_id
        data_type = request.data_type

        match data_type:
            case "temp":
                measure_collection = self.db["temp_data"]
            case "press":
                measure_collection = self.db["press_data"]

        try: 
            list_of_measures = list(measure_collection.find({"sensor_id":int(sensor_id)}))
        except PyMongoError as e:
            print(f"An error occurred: {e}")
            sys.exit(-1)
        else:
            sum = 0
            for measure in list_of_measures:
                sum += measure["data"]

        if len(list_of_measures) != 0:
            mean_value = sum/len(list_of_measures)
        else:
            mean_value = 0        
        
        return s_pb2.StringMessage(value=str(mean_value))
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    s_pb2_grpc.add_statisticServicer_to_server(StatisticsServicer(), server)

    server.add_insecure_port("[::]:50051")
    
    server.start()
    print("[STATISTICS]✅ Server started ")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()