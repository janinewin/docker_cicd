from concurrent import futures
import logging
import math
import time

import grpc
# from . import ml_pb2, ml_pb2_grpc
import ml_pb2, ml_pb2_grpc
# import route_guide_pb2_grpc
# import route_guide_resources


class ApiServicer(ml_pb2_grpc.ApiServicer):
    """Provides methods that implement functionality of ml_pb2 server."""

    def __init__(self):
        pass

    def MapFaces(self, request, context):
        # Do some actual face recognition
        print(request)
        print(f"Path {request.path}")
        
        coordinates = [
            {"x": 1, "y": 2},
            {"x": 3, "y": 10}
        ]

        faces = ml_pb2.Faces()
        faces.coordinates.extend([
            ml_pb2.Coordinate(x=coord["x"], y=coord["y"])
            for coord in coordinates
        ])

        return faces


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ml_pb2_grpc.add_ApiServicer_to_server(ApiServicer(), server)
    port = 50051
    print(f"Serving on port {port}")
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
