include ../../make.inc

IMG=lewagon/hnstream:0.1.0

build:
	docker build -t $(IMG) .

proto1:
	@poetry run python -m grpc_tools.protoc -I./proto --python_out=./hnstream/pyproto --grpc_python_out=./hnstream/pyproto ./proto/server.proto

proto2-mac:
	@sed -i '' 's/import server_pb2 as server__pb2/from hnstream.pyproto import server_pb2 as server__pb2/g' ./hnstream/pyproto/server_pb2_grpc.py

proto2:
	@sed -i 's/import server_pb2 as server__pb2/from hnstream.pyproto import server_pb2 as server__pb2/g' ./hnstream/pyproto/server_pb2_grpc.py


genproto: proto1 proto2

# sed works slightly differently on MacOS
genproto-mac: proto1 protoc2-mac
