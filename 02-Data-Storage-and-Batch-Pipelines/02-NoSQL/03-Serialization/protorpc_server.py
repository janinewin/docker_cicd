from src.grpc import api_pb2_grpc, proto_rpc
from concurrent import futures
import grpc


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    api_pb2_grpc.add_ApiServicer_to_server(proto_rpc.Api(), server)
    port = 50051
    print(f"Serving the gRPC server on port {port}")
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
