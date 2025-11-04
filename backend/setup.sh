#!/bin/bash
# Setup script for the test project

echo "Setting up test project..."

# Wait for database
echo "Waiting for database..."
sleep 5

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Generate proto files
echo "Generating proto files..."
python manage.py generateproto

echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update hello_app/serializers.py to import generated proto classes"
echo "2. Start the server: python manage.py grpcrunaioserver --dev"
echo "3. Test with: python test_client.py"

