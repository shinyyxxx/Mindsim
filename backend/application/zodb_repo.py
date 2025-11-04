"""
ZODB repository for storing flexible properties.
"""
from ZODB import DB
from ZODB.FileStorage import FileStorage
import persistent
import transaction
import uuid
from django.conf import settings


# Initialize ZODB storage
_storage = FileStorage(str(settings.ZODB_STORAGE_PATH))
_db = DB(_storage)
_conn = _db.open()
_root = _conn.root()


class Properties(persistent.Persistent):
    """Persistent object to store flexible properties."""
    
    def __init__(self, data: dict):
        self.data = data


def save_properties(data: dict) -> str:
    """
    Save properties to ZODB and return the key.
    
    Args:
        data: Dictionary of properties to store
        
    Returns:
        str: Key to retrieve the properties later
    """
    key = uuid.uuid4().hex
    _root[key] = Properties(data)
    transaction.commit()
    return key


def get_properties(key: str) -> dict | None:
    """
    Retrieve properties from ZODB by key.
    
    Args:
        key: ZODB key
        
    Returns:
        dict or None: Properties dictionary or None if not found
    """
    obj = _root.get(key)
    if obj:
        return getattr(obj, "data", None)
    return None


def delete_properties(key: str) -> bool:
    """
    Delete properties from ZODB.
    
    Args:
        key: ZODB key
        
    Returns:
        bool: True if deleted, False if not found
    """
    if key in _root:
        del _root[key]
        transaction.commit()
        return True
    return False

