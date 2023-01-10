import streaming_pb2
import streaming_pb2_grpc
import grpc
from concurrent import futures
import time

class NumberStreamService(streaming_pb2_grpc.NumberStreamServiceServicer):
    def GetNumbers(self, request, context):
        for i in range(1, 1000):
            yield streaming_pb2.GetNumbersResponse(value=i)

# Create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
streaming_pb2_grpc.add_NumberStreamServiceServicer_to_server(NumberStreamService(), server)
server.add_insecure_port('[::]:50051')
server.start()
print('Running server')
server.wait_for_termination()
