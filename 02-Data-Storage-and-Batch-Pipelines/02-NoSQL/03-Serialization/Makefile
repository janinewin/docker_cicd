include ../../../make.inc

compile-proto: compile-proto-1 compile-proto-2-linux

compile-proto-macos: compile-proto-1 compile-proto-2-macos

compile-proto-1:
	@echo "Compiled the files into lwapi/api_pb2.py and lwapi/api_pb2_grpc.py"
	python -m grpc_tools.protoc -I./protos/ --python_out=./lwapi/ --grpc_python_out=./lwapi/ ./protos/api.proto

compile-proto-2-linux:
	sed -i 's/import api_pb2 as api__pb2/from lwapi import api_pb2 as api__pb2/g' ./lwapi/api_pb2_grpc.py

compile-proto-2-macos:
	# We need this corner case as `sed` on Mac doesn't behave exactly like `sed` on Linux for the saddest reasons
	sed -i '' 's/import api_pb2 as api__pb2/from lwapi import api_pb2 as api__pb2/g' ./lwapi/api_pb2_grpc.py

test: pytest-and-write-output
