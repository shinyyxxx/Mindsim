
from django_socio_grpc import generics
from .models import Hello
from .serializers import HelloProtoSerializer


class HelloService(generics.AsyncModelService):

    queryset = Hello.objects.all()
    serializer_class = HelloProtoSerializer

