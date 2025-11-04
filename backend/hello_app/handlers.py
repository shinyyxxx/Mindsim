from django_socio_grpc.services.app_handler_registry import AppHandlerRegistry
from .services import HelloService


def grpc_handlers(server):
    app_registry = AppHandlerRegistry("hello_app", server)
    app_registry.register(HelloService)

