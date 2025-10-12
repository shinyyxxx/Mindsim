from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import ZODB
from ZODB.DB import DB
from ZODB.FileStorage import FileStorage
import transaction

from django.conf import settings


_db: Optional[DB] = None


def get_db() -> DB:
    global _db
    if _db is None:
        file_path = settings.ZODB_FILE_PATH
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        storage = FileStorage(file_path)
        _db = DB(storage)
    return _db


def open_connection():
    db = get_db()
    connection = db.open()
    root = connection.root()
    return connection, root


@dataclass
class ZODBContext:
    connection: any
    root: any


class ZODBManager:
    def __enter__(self) -> ZODBContext:
        self.connection, self.root = open_connection()
        return ZODBContext(connection=self.connection, root=self.root)

    def __exit__(self, exc_type, exc, tb):
        if exc is None:
            transaction.commit()
        else:
            transaction.abort()
        self.connection.close()


