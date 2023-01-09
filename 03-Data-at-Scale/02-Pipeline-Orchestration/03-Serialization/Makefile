include ../../../make.inc

compile-proto:
	@echo "Compiled the files into src/generated_proto/api_pb2.py and src/generated_proto/api_pb2_grpc.py"
	python -m grpc_tools.protoc -I./src/protos/ --python_out=./src/generated_proto/ --grpc_python_out=./src/generated_proto/ ./src/protos/api.proto

test: pytest-and-write-output
