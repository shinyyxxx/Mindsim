"""
Simple test client that works WITHOUT needing Django/GDAL installed locally.
This just sends gRPC requests to the Docker container.
"""
import asyncio
import grpc

# Import generated proto (after generateproto)
try:
    from hello_app.grpc.hello_app_pb2 import HelloRequest, HelloListRequest, HelloRetrieveRequest
    from hello_app.grpc.hello_app_pb2_grpc import HelloControllerStub
except ImportError:
    print("ERROR: Proto files not found!")
    print("Please run: docker exec test-backend-1 python manage.py generateproto")
    exit(1)


async def test_create_hello():
    """Test creating a Hello object."""
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = HelloControllerStub(channel)
        
        # Create a 3D point in WKT format: SRID=4326;POINT Z (lon lat elevation)
        location_wkt = "SRID=4326;POINT Z (103.8520 1.2908 15)"
        
        request = HelloRequest(
            message="Hello from simple Python client!",
            location=location_wkt
        )
        
        try:
            response = await stub.Create(request)
            print(f"[OK] Created Hello: {response.id}")
            print(f"  Message: {response.message}")
            print(f"  Properties key: {response.properties_key}")
            return response.id
        except Exception as e:
            print(f"[ERROR] Error creating Hello: {e}")
            return None


async def test_list_hello():
    """Test listing Hello objects."""
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = HelloControllerStub(channel)
        request = HelloListRequest()
        
        try:
            response = await stub.List(request)
            print(f"\n[OK] Found {len(response.results)} Hello objects:")
            for hello in response.results:
                print(f"  - {hello.message} ({hello.id})")
        except Exception as e:
            print(f"[ERROR] Error listing Hello: {e}")


async def test_retrieve_hello(hello_id: str):
    """Test retrieving a specific Hello object."""
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = HelloControllerStub(channel)
        
        try:
            request = HelloRetrieveRequest(id=hello_id)
            response = await stub.Retrieve(request)
            print(f"\n[OK] Retrieved Hello:")
            print(f"  ID: {response.id}")
            print(f"  Message: {response.message}")
            print(f"  Properties key: {response.properties_key}")
        except Exception as e:
            print(f"[ERROR] Error retrieving Hello: {e}")


if __name__ == "__main__":
    print("=" * 50)
    print("Simple Hello gRPC Test Client (No Django needed!)")
    print("=" * 50)
    print("\nMake sure the gRPC server is running:")
    print("  docker-compose up backend")
    print()
    
    hello_id = asyncio.run(test_create_hello())
    asyncio.run(test_list_hello())
    
    if hello_id:
        asyncio.run(test_retrieve_hello(hello_id))
    
    print("\n" + "=" * 50)
    print("Tests complete!")

