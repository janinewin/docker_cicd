# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tapi.proto\"\r\n\x0bTimeRequest\"/\n\x0cTimeResponse\x12\t\n\x01h\x18\x01 \x01(\x03\x12\t\n\x01m\x18\x02 \x01(\x03\x12\t\n\x01s\x18\x03 \x01(\x03\"-\n\x0cRuralRequest\x12\x0c\n\x04year\x18\x01 \x01(\x03\x12\x0f\n\x07\x63ountry\x18\x02 \x01(\t\"\x1e\n\rRuralResponse\x12\r\n\x05value\x18\x01 \x01(\x01\x32t\n\x03\x41pi\x12)\n\x08get_time\x12\x0c.TimeRequest\x1a\r.TimeResponse\"\x00\x12\x42\n\x1fget_rural_population_percentage\x12\r.RuralRequest\x1a\x0e.RuralResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'api_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TIMEREQUEST._serialized_start=13
  _TIMEREQUEST._serialized_end=26
  _TIMERESPONSE._serialized_start=28
  _TIMERESPONSE._serialized_end=75
  _RURALREQUEST._serialized_start=77
  _RURALREQUEST._serialized_end=122
  _RURALRESPONSE._serialized_start=124
  _RURALRESPONSE._serialized_end=154
  _API._serialized_start=156
  _API._serialized_end=272
# @@protoc_insertion_point(module_scope)