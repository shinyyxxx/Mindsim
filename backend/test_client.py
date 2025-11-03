"""
Simple test client to test the Hello gRPC service.
This will work after running generateproto and starting the server.
"""
import asyncio
import grpc
from django.contrib.gis.geos import Point

# Import generated proto (will be available after generateproto)
# from hello_app.grpc.hello_app_pb2 import HelloRequest, HelloListRequest
# from hello_app.grpc.hello_app_pb2_grpc import HelloControllerStub


async def test_create_hello():
    """Test creating a Hello object."""
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        # stub = HelloControllerStub(channel)
        
        # Create a 3D point (lon, lat, elevation)
        point = Point(103.8520, 1.2908, 15.0, srid=4326)
        
        # This is example code - uncomment after generateproto
        # request = HelloRequest(
        #     message="Hello from Python client!",
        #     geometry_wkb=bytes(point.wkb),
        #     geometry_srid=4326,
        #     properties={"color": "blue", "size": "large"}
        # )
        # 
        # response = await stub.Create(request)
        # print(f"Created Hello: {response.id}")
        # print(f"Message: {response.message}")
        # print(f"Properties key: {response.properties_key}")
        # return response.id
        
        print("Test client - uncomment code after running generateproto")
        print(f"Point created: {point}")


async def test_list_hello():
    """Test listing Hello objects."""
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        # stub = HelloControllerStub(channel)
        # request = HelloListRequest()
        # response = await stub.List(request)
        # print(f"Found {len(response.results)} Hello objects")
        # for hello in response.results:
        #     print(f"  - {hello.message} ({hello.id})")
        print("List test - uncomment code after running generateproto")


if __name__ == "__main__":
    print("Running test client...")
    print("Note: Make sure you've:")
    print("1. Run migrations")
    print("2. Run generateproto")
    print("3. Started the gRPC server")
    print()
    asyncio.run(test_create_hello())
    asyncio.run(test_list_hello())

