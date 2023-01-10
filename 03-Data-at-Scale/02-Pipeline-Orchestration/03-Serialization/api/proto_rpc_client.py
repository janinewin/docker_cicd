import argparse
import grpc
from api.generated_proto import api_pb2
from api.generated_proto import api_pb2_grpc

def run_client():
    with grpc.insecure_channel('localhost:50052') as channel:

        pass  # YOUR CODE HERE

if __name__ == "__main__":
    run_client()
