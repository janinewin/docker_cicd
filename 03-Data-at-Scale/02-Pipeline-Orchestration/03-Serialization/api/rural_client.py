import grpc
from api.generated_proto import api_pb2
from api.generated_proto import api_pb2_grpc


def run_client():

    # Create a gRPC channel
    channel = grpc.insecure_channel('localhost:50053')

    # Create a stub for the CountryYearService
    stub = api_pb2_grpc.CountryYearServiceStub(channel)

    pass  # YOUR CODE HERE

    # Print the response
    print(response.value)

if __name__ == "__main__":
    run_client()
