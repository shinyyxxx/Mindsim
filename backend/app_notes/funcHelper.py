from datetime import datetime
from django.db import connection
from app_notes.models import SRID_3D, MentalSphere, Mind
from app_notes.mentalSphereObject import MentalSphereObject, MindObject
from zodb.zodb_management import get_connection
import transaction
import json


def create_spatial_data(position=None, rotation=None, scale=None, object_type='mentalsphere'):
    if position is None:
        position = [0, 0, 0]
    if rotation is None:
        rotation = [0, 0, 0]
    if scale is None:
        scale = 1.0
    
    with connection.cursor() as cursor:
        cursor.execute(f"""
            INSERT INTO app_notes_{object_type}spatialdata (position, rotation, scale, created_at, updated_at)
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


def update_spatial_data(spatial_id, position=None, rotation=None, scale=None, object_type='mentalsphere'):
    pos_wkt = (
        f"SRID={SRID_3D};POINT Z({position[0]} {position[1]} {position[2]})"
        if position is not None
        else None
    )
    rot_wkt = (
        f"SRID={SRID_3D};POINT Z({rotation[0]} {rotation[1]} {rotation[2]})"
        if rotation is not None
        else None
    )

    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            UPDATE app_notes_{object_type}spatialdata
            SET
                position = COALESCE(
                    ST_GeomFromEWKT(%s),
                    position
                ),
                rotation = COALESCE(
                    ST_GeomFromEWKT(%s),
                    rotation
                ),
                scale = COALESCE(%s, scale),
                updated_at = NOW()
            WHERE id = %s
            """,
            [pos_wkt, rot_wkt, scale, spatial_id],
        )


def get_spatial_data(spatial_id, object_type='mentalsphere'):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT ST_AsEWKT(position), ST_AsEWKT(rotation), scale
            FROM app_notes_{object_type}spatialdata
            WHERE id=%s
        """, [spatial_id])
        result = cursor.fetchone()
        
        if not result:
            return None

        position_ewkt, rotation_ewkt, scale = result
        
        position_coords = [float(c) for c in position_ewkt.split('(')[1].rstrip(')').split()]
        rotation_coords = [float(c) for c in rotation_ewkt.split('(')[1].rstrip(')').split()]
        scale = float(scale)

        return {
            'position': position_coords,
            'rotation': rotation_coords,
            'scale': scale
        }



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
    # under development
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
                rotation=sphere_data.get('rotation'),
                scale=sphere_data.get('scale')
            )
        
        sphere.set_updated_at(datetime.now())
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
        'image': sphere.get_image(),
        'rec_status': sphere.get_rec_status(),
        'created_by': sphere.get_created_by(),
        'position': spatial_data['position'],
        'rotation': spatial_data['rotation'],
        'scale': spatial_data['scale'],
        'created_at': sphere.get_created_at().isoformat() if sphere.get_created_at() else None,
        'updated_at': sphere.get_updated_at().isoformat() if sphere.get_updated_at() else None
    }


def create_mind_zodb(root, mind_data):
    try:
        if not hasattr(root, 'minds'):
            root.minds = {}
        
        mind_id = get_mind_id(root)
        current_date = datetime.now()

        spatial_data_id = create_spatial_data(
            position=mind_data.get('position', [0, 0, 0]),
            rotation=mind_data.get('rotation', [0, 0, 0]),
            scale=mind_data.get('scale', 1.0),
            object_type='mind'
        )

        # Create Mind object in ZODB
        root.minds[mind_id] = MindObject(
            id=mind_id,
            name=mind_data.get('name', ''),
            detail=mind_data.get('detail', ''),
            color=mind_data.get('color', '#FFFFFF'),
            spatial_data_id=spatial_data_id,
            rec_status=mind_data.get('rec_status', True),
            created_by=mind_data.get('created_by'),
            mental_sphere_ids=mind_data.get('mental_sphere_ids', []),
            created_at=current_date
        )
        
        transaction.commit()
        return mind_id
    except Exception:
        transaction.abort()
        raise


def update_mind_zodb(root, mind_id, mind_data):
    try:
        if not hasattr(root, 'minds'):
            root.minds = {}
        
        if mind_id not in root.minds:
            raise ValueError(f"Update Failed : Mind with ID {mind_id} not found")
        
        mind = root.minds[mind_id]
        
        if 'name' in mind_data:
            mind.set_name(mind_data['name'])
        if 'detail' in mind_data:
            mind.set_detail(mind_data['detail'])
        if 'color' in mind_data:
            mind.set_color(mind_data['color'])
        if 'rec_status' in mind_data:
            mind.set_rec_status(mind_data['rec_status'])
        if 'position' or 'rotation' or 'scale' in mind_data:
            update_spatial_data(
                mind.get_spatial_data_id(),
                position=mind_data['position'] if 'position' in mind_data else None,
                rotation=mind_data['rotation'] if 'rotation' in mind_data else None,
                scale=mind_data['scale'] if 'scale' in mind_data else None,
                object_type='mind'
            )
        mind.set_updated_at(datetime.now())
        transaction.commit()
        return mind_id
    except Exception:
        transaction.abort()
        raise


def get_mind_zodb(root, mind_id):

    if not hasattr(root, 'minds') or mind_id not in root.minds:
        return None
    
    mind = root.minds[mind_id]

    mind_spatial = get_spatial_data(mind.get_spatial_data_id(), object_type='mind')
    
    return {
        'id': mind.get_id(),
        'name': mind.get_name(),
        'detail': mind.get_detail(),
        'color': mind.get_color(),
        'rec_status': mind.get_rec_status(),
        'position': mind_spatial['position'],
        'rotation': mind_spatial['rotation'],
        'scale': mind_spatial['scale'],
        'created_by': mind.get_created_by(),
        'mental_sphere_ids': mind.get_mental_sphere_ids(),
        'created_at': mind.get_created_at().isoformat() if mind.get_created_at() else None,
        'updated_at': mind.get_updated_at().isoformat() if mind.get_updated_at() else None
    }


def add_mental_spheres_to_mind(root, mind_id, sphere_ids):
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
