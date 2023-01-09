import grpc
import streaming_pb2
import streaming_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = streaming_pb2_grpc.NumberStreamServiceStub(channel)

response_iterator = stub.GetNumbers(streaming_pb2.GetNumbersRequest())

for response in response_iterator:
    print(response.value)

channel.close()
