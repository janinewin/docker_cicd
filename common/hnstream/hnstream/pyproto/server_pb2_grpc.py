# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from hnstream.pyproto import server_pb2 as server__pb2


class HnstreamerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetNextComments = channel.unary_unary(
            "/hnstream.Hnstreamer/GetNextComments",
            request_serializer=server__pb2.GetNextRequest.SerializeToString,
            response_deserializer=server__pb2.GetNextCommentsResponse.FromString,
        )
        self.GetNextStories = channel.unary_unary(
            "/hnstream.Hnstreamer/GetNextStories",
            request_serializer=server__pb2.GetNextRequest.SerializeToString,
            response_deserializer=server__pb2.GetNextStoriesResponse.FromString,
        )


class HnstreamerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetNextComments(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetNextStories(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_HnstreamerServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "GetNextComments": grpc.unary_unary_rpc_method_handler(
            servicer.GetNextComments,
            request_deserializer=server__pb2.GetNextRequest.FromString,
            response_serializer=server__pb2.GetNextCommentsResponse.SerializeToString,
        ),
        "GetNextStories": grpc.unary_unary_rpc_method_handler(
            servicer.GetNextStories,
            request_deserializer=server__pb2.GetNextRequest.FromString,
            response_serializer=server__pb2.GetNextStoriesResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler("hnstream.Hnstreamer", rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class Hnstreamer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetNextComments(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/hnstream.Hnstreamer/GetNextComments",
            server__pb2.GetNextRequest.SerializeToString,
            server__pb2.GetNextCommentsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetNextStories(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/hnstream.Hnstreamer/GetNextStories",
            server__pb2.GetNextRequest.SerializeToString,
            server__pb2.GetNextStoriesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
