from generated_proto import api_pb2, api_pb2_grpc

import grpc
from concurrent import futures
import time
from datetime import datetime

class TimeService(api_pb2_grpc.TimeServiceServicer):
    def GetTime(self, request, context):
        pass  # YOUR CODE HERE
