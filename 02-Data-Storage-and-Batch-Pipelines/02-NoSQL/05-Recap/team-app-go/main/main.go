package main

import (
	"context"
	"fmt"
	"log"
	"time"

	pb "example/ok"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func main() {
	addr := "localhost:50051"
	conn, err := grpc.Dial(addr, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	c := pb.NewApiClient(conn)

	// Contact the server and print out its response.
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	r, err := c.MapFaces(ctx, &pb.Image{
		Path: "/home/ubuntu/whatever.png",
	})
	if err != nil {
		log.Fatalf("could not greet: %v", err)
	}
	for _, coord := range r.GetCoordinates() {
		fmt.Printf("X=%d, Y=%d\n", coord.X, coord.Y)
	}

}

// import (
// 	"context"
// 	"flag"
// 	"log"
// 	"time"

// 	"google.golang.org/grpc"
// 	"google.golang.org/grpc/credentials/insecure"
// 	pb "google.golang.org/grpc/examples/helloworld/helloworld"
// )

// const (
// 	defaultName = "world"
// )

// var (
// 	addr = flag.String("addr", "localhost:50051", "the address to connect to")
// 	name = flag.String("name", defaultName, "Name to greet")
// )

// func main() {
// 	flag.Parse()
// 	// Set up a connection to the server.
// 	conn, err := grpc.Dial(*addr, grpc.WithTransportCredentials(insecure.NewCredentials()))
// 	if err != nil {
// 		log.Fatalf("did not connect: %v", err)
// 	}
// 	defer conn.Close()
// 	c := pb.NewGreeterClient(conn)

// 	// Contact the server and print out its response.
// 	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
// 	defer cancel()
// 	r, err := c.SayHello(ctx, &pb.HelloRequest{Name: *name})
// 	if err != nil {
// 		log.Fatalf("could not greet: %v", err)
// 	}
// 	log.Printf("Greeting: %s", r.GetMessage())
// }
