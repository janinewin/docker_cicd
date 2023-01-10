# Import datetime
# IMPORT YOUR PACKAGES HERE

from concurrent import futures
import grpc
from grpc import api_pb2, api_pb2_grpc
import rural

class Api(api_pb2_grpc.ApiServicer):

  def get_time(self, request, context):
    # Replace `dt = None` with the current time
    dt = None
    pass  # YOUR CODE HERE
    return api_pb2.TimeResponse(h=dt.hour, m=dt.minute, s=dt.second)

  def get_rural_population_percentage(self, request, context):
    dataset = rural.load_rural_csv()
    # Fill the `value` of the rural population percentage for the right country and year
    value = 0
    pass  # YOUR CODE HERE

    return api_pb2.RuralResponse(value=value)
