from datetime import datetime
from django.db import connection
from app_notes.models import SRID_3D, MentalSphere, Mind
from app_notes.mentalSphereObject import MentalSphereObject, MindObject
from zodb.zodb_management import get_connection
import transaction
import json


def create_spatial_data(position=None, rotation=None, scale=None):
    if position is None:
        position = [0, 0, 0]
    if rotation is None:
        rotation = [0, 0, 0]
    if scale is None:
        scale = 1.0
    
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO app_notes_mentalspherespatialdata (position, rotation, scale, created_at, updated_at)
            VALUES (
                ST_GeomFromEWKT(%s),
                ST_GeomFromEWKT(%s),
                %s,
                NOW(),
                NOW()
            )
            RETURNING id
        """, [
            f'SRID={SRID_3D};POINT Z({position[0]} {position[1]} {position[2]})',
            f'SRID={SRID_3D};POINT Z({rotation[0]} {rotation[1]} {rotation[2]})',
            scale
        ])
        spatial_id = cursor.fetchone()[0]
    return spatial_id


def update_spatial_data(spatial_id, position=None, rotation=None):
    """
    Update existing spatial data in PostGIS
    
    Args:
        spatial_id: The ID of the spatial data to update
        position: [x, y, z] array for position
        rotation: [x, y, z] array for rotation degrees
    """
    with connection.cursor() as cursor:
        if position and rotation:
            cursor.execute("""
                UPDATE app_notes_mentalspherespatialdata
                SET 
                    position = ST_GeomFromEWKT(%s),
                    rotation = ST_GeomFromEWKT(%s),
                    updated_at = NOW()
                WHERE id = %s
            """, [
                f'SRID={SRID_3D};POINT Z({position[0]} {position[1]} {position[2]})',
                f'SRID={SRID_3D};POINT Z({rotation[0]} {rotation[1]} {rotation[2]})',
                spatial_id
            ])
        elif position:
            cursor.execute("""
                UPDATE app_notes_mentalspherespatialdata
                SET 
                    position = ST_GeomFromEWKT(%s),
                    updated_at = NOW()
                WHERE id = %s
            """, [
                f'SRID={SRID_3D};POINT Z({position[0]} {position[1]} {position[2]})',
                spatial_id
            ])
        elif rotation:
            cursor.execute("""
                UPDATE app_notes_mentalspherespatialdata
                SET 
                    rotation = ST_GeomFromEWKT(%s),
                    updated_at = NOW()
                WHERE id = %s
            """, [
                f'SRID={SRID_3D};POINT Z({rotation[0]} {rotation[1]} {rotation[2]})',
                spatial_id
            ])


def get_spatial_data(spatial_id):
    """
    Get spatial data from PostGIS
    
    Args:
        spatial_id: The ID of the spatial data
        
    Returns:
        dict: Dictionary with 'position' and 'rotation' as [x, y, z] arrays
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ST_AsEWKT(position), ST_AsEWKT(rotation) 
            FROM app_notes_mentalspherespatialdata 
            WHERE id=%s
        """, [spatial_id])
        result = cursor.fetchone()
        
        if not result:
            return None
        
        position_ewkt, rotation_ewkt = result
        
        # Parse EWKT format: 'SRID=4979;POINT Z(x y z)'
        position_coords = [float(c) for c in position_ewkt.split('(')[1].rstrip(')').split()]
        rotation_coords = [float(c) for c in rotation_ewkt.split('(')[1].rstrip(')').split()]
        
        return {
            'position': position_coords,
            'rotation': rotation_coords
        }


def delete_spatial_data(spatial_id):
    """Delete spatial data from PostGIS"""
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM app_notes_mentalspherespatialdata WHERE id=%s", [spatial_id])


def get_mental_sphere_id(root):
    """Get the next available ID for MentalSphere in ZODB"""
    if not hasattr(root, 'mentalSpheres') or not root.mentalSpheres:
        return 1
    existing_ids = [int(key) for key in root.mentalSpheres.keys() if str(key).isdigit()]
    return max(existing_ids) + 1 if existing_ids else 1


def get_mind_id(root):
    if not hasattr(root, 'minds') or not root.minds:
        return 1
    existing_ids = [int(key) for key in root.minds.keys() if str(key).isdigit()]
    return max(existing_ids) + 1 if existing_ids else 1


def create_mental_sphere_zodb(root, sphere_data):
    try:
        if not hasattr(root, 'mentalSpheres'):
            root.mentalSpheres = {}
        
        sphere_id = get_mental_sphere_id(root)
        current_date = datetime.now()
        
        spatial_data_id = create_spatial_data(
            position=sphere_data.get('position', [0, 0, 0]),
            rotation=sphere_data.get('rotation', [0, 0, 0]),
            scale=sphere_data.get('scale', 1.0)
        )
        
        root.mentalSpheres[sphere_id] = MentalSphereObject(
            id=sphere_id,
            name=sphere_data.get('name', ''),
            detail=sphere_data.get('detail', ''),
            color=sphere_data.get('color', '#FFFFFF'),
            image=sphere_data.get('image', ''),
            rec_status=sphere_data.get('rec_status', True),
            spatial_data_id=spatial_data_id,
            created_by=sphere_data.get('created_by'),
            created_at=current_date
        )
        
        transaction.commit()
        return sphere_id
    except Exception:
        transaction.abort()
        raise


def update_mental_sphere_zodb(root, sphere_id, sphere_data):
    """
    Update a MentalSphere in ZODB
    
    Args:
        root: ZODB root object
        sphere_id: ID of the sphere to update
        sphere_data: Dictionary with updated sphere information
    """
    try:
        if not hasattr(root, 'mentalSpheres') or sphere_id not in root.mentalSpheres:
            raise ValueError(f"MentalSphere with ID {sphere_id} not found")
        
        sphere = root.mentalSpheres[sphere_id]
        
        # Update fields
        if 'name' in sphere_data:
            sphere.set_name(sphere_data['name'])
        if 'detail' in sphere_data:
            sphere.set_detail(sphere_data['detail'])
        if 'texture' in sphere_data:
            sphere.set_texture(sphere_data['texture'])
        if 'color' in sphere_data:
            sphere.set_color(sphere_data['color'])
        if 'rec_status' in sphere_data:
            sphere.set_rec_status(sphere_data['rec_status'])
        
        # Update spatial data if provided
        if 'position' in sphere_data or 'rotation' in sphere_data:
            update_spatial_data(
                sphere.get_position_id(),
                position=sphere_data.get('position'),
                rotation=sphere_data.get('rotation')
            )
        
        sphere.set_updated_at(datetime.now())
        transaction.commit()
    except Exception:
        transaction.abort()
        raise


def delete_mental_sphere_zodb(root, sphere_id):
    """
    Delete a MentalSphere from ZODB and its spatial data
    
    Args:
        root: ZODB root object
        sphere_id: ID of the sphere to delete
    """
    try:
        if not hasattr(root, 'mentalSpheres') or sphere_id not in root.mentalSpheres:
            raise ValueError(f"MentalSphere with ID {sphere_id} not found")
        
        sphere = root.mentalSpheres[sphere_id]
        
        # Delete spatial data from PostGIS
        if sphere.get_position_id():
            delete_spatial_data(sphere.get_position_id())
        
        # Delete from ZODB
        del root.mentalSpheres[sphere_id]
        transaction.commit()
    except Exception:
        transaction.abort()
        raise


def get_mental_sphere_zodb(root, sphere_id):
    if not hasattr(root, 'mentalSpheres') or sphere_id not in root.mentalSpheres:
        return None
    
    sphere = root.mentalSpheres[sphere_id]
    spatial_data = get_spatial_data(sphere.get_spatial_data_id())
    
    return {
        'id': sphere.get_id(),
        'name': sphere.get_name(),
        'detail': sphere.get_detail(),
        'color': sphere.get_color(),
        'image': sphere.get_texture(),
        'rec_status': sphere.get_rec_status(),
        'created_by': sphere.get_created_by(),
        'position': spatial_data['position'] if spatial_data else [0, 0, 0],
        'rotation': spatial_data['rotation'] if spatial_data else [0, 0, 0],
        'created_at': sphere.get_created_at().isoformat() if sphere.get_created_at() else None,
        'updated_at': sphere.get_updated_at().isoformat() if sphere.get_updated_at() else None
    }


def create_mind_zodb(root, mind_data):
    try:
        # Initialize minds if it doesn't exist
        if not hasattr(root, 'minds'):
            root.minds = {}
        
        mind_id = get_mind_id(root)
        current_date = datetime.now()
        
        # Create Mind object in ZODB
        root.minds[mind_id] = MindObject(
            id=mind_id,
            name=mind_data.get('name', ''),
            detail=mind_data.get('detail', ''),
            position=mind_data.get('position', [0, 0, 0]),
            rec_status=mind_data.get('rec_status', True),
            created_by_id=mind_data.get('created_by_id'),
            mental_sphere_ids=mind_data.get('mental_sphere_ids', []),
            created_at=current_date
        )
        
        transaction.commit()
        return mind_id
    except Exception:
        transaction.abort()
        raise


def update_mind_zodb(root, mind_id, mind_data):
    """
    Update a Mind in ZODB (upsert operation)
    
    Args:
        root: ZODB root object
        mind_id: ID of the mind to update (creates new if doesn't exist)
        mind_data: Dictionary with updated mind information
        
    Returns:
        int: The ID of the updated/created Mind
    """
    try:
        if not hasattr(root, 'minds'):
            root.minds = {}
        
        # If mind doesn't exist, create it
        if mind_id not in root.minds:
            mind_data['created_by_id'] = mind_data.get('created_by_id')
            return create_mind_zodb(root, mind_data)
        
        # Update existing mind
        mind = root.minds[mind_id]
        
        if 'name' in mind_data:
            mind.set_name(mind_data['name'])
        if 'detail' in mind_data:
            mind.set_detail(mind_data['detail'])
        if 'position' in mind_data:
            mind.set_position(mind_data['position'])
        if 'rec_status' in mind_data:
            mind.set_rec_status(mind_data['rec_status'])
        
        mind.set_updated_at(datetime.now())
        transaction.commit()
        return mind_id
    except Exception:
        transaction.abort()
        raise


def get_mind_zodb(root, mind_id):
    """
    Get a Mind from ZODB
    
    Args:
        root: ZODB root object
        mind_id: ID of the mind
        
    Returns:
        dict: Dictionary with mind data
    """
    if not hasattr(root, 'minds') or mind_id not in root.minds:
        return None
    
    mind = root.minds[mind_id]
    
    return {
        'id': mind.get_id(),
        'name': mind.get_name(),
        'detail': mind.get_detail(),
        'position': mind.get_position(),
        'rec_status': mind.get_rec_status(),
        'created_by_id': mind.get_created_by_id(),
        'mental_sphere_ids': mind.get_mental_sphere_ids(),
        'created_at': mind.get_created_at().isoformat() if mind.get_created_at() else None,
        'updated_at': mind.get_updated_at().isoformat() if mind.get_updated_at() else None
    }


def add_mental_spheres_to_mind(root, mind_id, sphere_ids):
    """
    Add mental spheres to a mind
    
    Args:
        root: ZODB root object
        mind_id: ID of the mind
        sphere_ids: List of sphere IDs to add
    """
    try:
        if not hasattr(root, 'minds') or mind_id not in root.minds:
            raise ValueError(f"Mind with ID {mind_id} not found")
        
        mind = root.minds[mind_id]
        
        for sphere_id in sphere_ids:
            mind.add_mental_sphere(sphere_id)
        
        mind.set_updated_at(datetime.now())
        transaction.commit()
    except Exception:
        transaction.abort()
        raise


def delete_mental_spheres_from_mind(root, mind_id, sphere_ids):
    """
    Remove mental spheres from a mind
    
    Args:
        root: ZODB root object
        mind_id: ID of the mind
        sphere_ids: List of sphere IDs to remove
    """
    try:
        if not hasattr(root, 'minds') or mind_id not in root.minds:
            raise ValueError(f"Mind with ID {mind_id} not found")
        
        mind = root.minds[mind_id]
        
        for sphere_id in sphere_ids:
            mind.remove_mental_sphere(sphere_id)
        
        mind.set_updated_at(datetime.now())
        transaction.commit()
    except Exception:
        transaction.abort()
        raise
