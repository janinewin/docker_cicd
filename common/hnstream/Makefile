build:
	docker build -t lewagon/hnstream:0.1.0 .

format:
	poetry run black .
	poetry run isort .

genproto:
	@poetry run python -m grpc_tools.protoc -I./proto --python_out=./hnstream/pyproto --grpc_python_out=./hnstream/pyproto ./proto/server.proto
	@sed -i '' 's/import server_pb2 as server__pb2/from hnstream.pyproto import server_pb2 as server__pb2/g' ./hnstream/pyproto/server_pb2_grpc.py
