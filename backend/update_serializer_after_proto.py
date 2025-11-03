"""
Helper script to update serializers.py after running generateproto.
This adds the proto_class imports and references.
"""
import os
import re

SERIALIZER_PATH = "hello_app/serializers.py"


def update_serializer():
    """Update serializer file with proto class imports."""
    
    if not os.path.exists(SERIALIZER_PATH):
        print(f"Error: {SERIALIZER_PATH} not found!")
        return False
    
    # Check if proto file exists
    proto_path = "hello_app/grpc/hello_app_pb2.py"
    if not os.path.exists(proto_path):
        print(f"Error: {proto_path} not found!")
        print("Please run: python manage.py generateproto")
        return False
    
    # Read current serializer
    with open(SERIALIZER_PATH, "r") as f:
        content = f.read()
    
    # Check if already updated
    if "from hello_app.grpc.hello_app_pb2 import" in content:
        print("Serializer already updated!")
        return True
    
    # Add imports after the existing imports
    import_line = "from hello_app.grpc.hello_app_pb2 import HelloResponse, HelloListResponse\n"
    
    # Find the right place to insert (after the comment about imports)
    lines = content.split("\n")
    insert_idx = None
    for i, line in enumerate(lines):
        if "# After running generateproto" in line or "# These will be auto-generated" in line:
            # Insert after the comment block
            insert_idx = i + 1
            # Remove comment line about imports
            if "# After running generateproto" in line:
                lines[i] = ""
            break
    
    if insert_idx is None:
        # Insert after last import
        for i, line in enumerate(lines):
            if line.startswith("from") or line.startswith("import"):
                insert_idx = i + 1
    
    if insert_idx:
        lines.insert(insert_idx, import_line)
    
    # Update the Meta class
    new_content = "\n".join(lines)
    
    # Add proto_class if not present
    if "proto_class = HelloResponse" not in new_content:
        new_content = re.sub(
            r'(class Meta:.*?fields = \[.*?\])',
            r'\1\n        proto_class = HelloResponse\n        proto_class_list = HelloListResponse',
            new_content,
            flags=re.DOTALL
        )
    
    # Write back
    with open(SERIALIZER_PATH, "w") as f:
        f.write(new_content)
    
    print(f"✓ Updated {SERIALIZER_PATH}")
    print("  - Added proto class imports")
    print("  - Added proto_class and proto_class_list to Meta")
    return True


if __name__ == "__main__":
    print("Updating serializer after proto generation...")
    if update_serializer():
        print("\n✓ Done! Your serializer is ready to use.")
    else:
        print("\n✗ Failed. Please check errors above.")

