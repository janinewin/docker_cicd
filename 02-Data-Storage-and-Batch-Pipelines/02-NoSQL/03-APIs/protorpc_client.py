import argparse
import grpc
from lwapi import api_pb2, api_pb2_grpc


def run_client():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = api_pb2_grpc.ApiStub(channel)
        response = stub.GetTime(api_pb2.TimeRequest())
        print(f"Api client received: h:{response.h} m:{response.m} s:{response.s}")


if __name__ == "__main__":
    run_client()
