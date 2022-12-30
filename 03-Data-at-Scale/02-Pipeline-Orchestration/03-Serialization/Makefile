include ../../../make.inc

compile-proto:
	@echo "Compiled the files into src/grpc/api_pb2.py and src/grpc/api_pb2_grpc.py"
	python -m grpc_tools.protoc -I./src/protos/ --python_out=./src/grpc/ --grpc_python_out=./src/grpc/ ./src/protos/api.proto

test: pytest-and-write-output
