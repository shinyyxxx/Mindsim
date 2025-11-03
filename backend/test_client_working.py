"""
Working test client - run this AFTER running generateproto and updating serializers.
"""
import asyncio
import grpc
import os
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings")
django.setup()

from django.contrib.gis.geos import Point

# Import generated proto (after generateproto)
try:
    from hello_app.grpc.hello_app_pb2 import HelloRequest, HelloListRequest
    from hello_app.grpc.hello_app_pb2_grpc import HelloControllerStub
except ImportError:
    print("ERROR: Proto files not found!")
    print("Please run: python manage.py generateproto")
    exit(1)


async def test_create_hello():
    """Test creating a Hello object."""
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = HelloControllerStub(channel)
        
        # Create a 3D point (lon, lat, elevation)
        point = Point(103.8520, 1.2908, 15.0, srid=4326)
        
        request = HelloRequest(
            message="Hello from Python client!",
            location=str(point)  # Convert Point to WKT string
        )
        
        try:
            response = await stub.Create(request)
            print(f"✓ Created Hello: {response.id}")
            print(f"  Message: {response.message}")
            print(f"  Properties key: {response.properties_key}")
            return response.id
        except Exception as e:
            print(f"✗ Error creating Hello: {e}")
            return None


async def test_list_hello():
    """Test listing Hello objects."""
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = HelloControllerStub(channel)
        request = HelloListRequest()
        
        try:
            response = await stub.List(request)
            print(f"\n✓ Found {len(response.results)} Hello objects:")
            for hello in response.results:
                print(f"  - {hello.message} ({hello.id})")
        except Exception as e:
            print(f"✗ Error listing Hello: {e}")


async def test_retrieve_hello(hello_id: str):
    """Test retrieving a specific Hello object."""
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = HelloControllerStub(channel)
        
        try:
            from hello_app.grpc.hello_app_pb2 import HelloRetrieveRequest
            request = HelloRetrieveRequest(id=hello_id)
            response = await stub.Retrieve(request)
            print(f"\n✓ Retrieved Hello:")
            print(f"  ID: {response.id}")
            print(f"  Message: {response.message}")
            print(f"  Properties key: {response.properties_key}")
        except Exception as e:
            print(f"✗ Error retrieving Hello: {e}")


if __name__ == "__main__":
    print("=" * 50)
    print("Testing Hello gRPC Service")
    print("=" * 50)
    print("\nMake sure the gRPC server is running:")
    print("  python manage.py grpcrunaioserver --dev")
    print()
    
    hello_id = asyncio.run(test_create_hello())
    asyncio.run(test_list_hello())
    
    if hello_id:
        asyncio.run(test_retrieve_hello(hello_id))
    
    print("\n" + "=" * 50)
    print("Tests complete!")

