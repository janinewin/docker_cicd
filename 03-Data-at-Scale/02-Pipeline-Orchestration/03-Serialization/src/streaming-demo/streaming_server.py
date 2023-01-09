import streaming_pb2
import streaming_pb2_grpc
import grpc
from concurrent import futures
import time

class NumberStreamService(streaming_pb2_grpc.NumberStreamServiceServicer):
    def GetNumbers(self, request, context):
        for i in range(1, 10):
            yield streaming_pb2.GetNumbersResponse(value=i)

# Create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
streaming_pb2_grpc.add_NumberStreamServiceServicer_to_server(NumberStreamService(), server)
server.add_insecure_port('[::]:50051')
server.start()

try:
    while True:
        print('Running server')
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
