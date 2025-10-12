from __future__ import annotations

from typing import Callable

import transaction

from .zodb import open_connection


class ZODBTransactionMiddleware:
    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request):
        connection, root = open_connection()
        request.zodb_connection = connection
        request.zodb_root = root
        try:
            response = self.get_response(request)
            transaction.commit()
            return response
        except Exception:
            transaction.abort()
            raise
        finally:
            connection.close()


