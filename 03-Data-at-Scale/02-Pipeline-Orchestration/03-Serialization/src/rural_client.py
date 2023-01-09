import grpc
import generated_proto.api_pb2 as api_pb2
import generated_proto.api_pb2_grpc as api_pb2_grpc


def run_client():

    # Create a gRPC channel
    channel = grpc.insecure_channel('localhost:50051')

    # Create a stub for the CountryYearService
    stub = api_pb2_grpc.CountryYearServiceStub(channel)


    pass  # YOUR CODE HERE

    # Print the response
    print(response.value)

if __name__ == "__main__":
    run_client()
