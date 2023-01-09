from src.generated_proto import api_pb2
from src.generated_proto import api_pb2_grpc

import grpc
from concurrent import futures
from datetime import datetime

class TimeService(api_pb2_grpc.TimeServiceServicer):
    def GetTime(self, request, context):
        pass  # YOUR CODE HERE

server.add_insecure_port('[::]:50052')
server.start()
print("server started running")
server.wait_for_termination()
