import json
from functools import wraps
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .models import MentalSphere, Mind
from .funcHelper import (
    create_mental_sphere_zodb,
    update_mental_sphere_zodb,
    delete_mental_sphere_zodb,
    get_mental_sphere_zodb,
    create_mind_zodb,
    update_mind_zodb,
    get_mind_zodb,
    add_mental_spheres_to_mind,
    delete_mental_spheres_from_mind
)
from zodb.zodb_management import get_connection


def get_request_data(request):
    try:
        if request.content_type == 'application/json':
            return json.loads(request.body)
        else:
            return request.POST
    except (json.JSONDecodeError, AttributeError):
        return request.POST


def require_auth(view_func):
    """Decorator to require authentication"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper


# ============= Mind API Methods =============

@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def get_mind(request):
    """
    Get Mind objects by ID list
    POST body: { "mind_id_list": [1, 2, 3] }
    Returns: { "minds": [...] }
    """
    try:
        data = get_request_data(request)
        mind_id_list = data.get('mind_id_list', [])
        
        if not isinstance(mind_id_list, list):
            return JsonResponse({'error': 'mind_id_list must be an array'}, status=400)
        
        _, root = get_connection()
        minds = []
        
        for mind_id in mind_id_list:
            mind_data = get_mind_zodb(root, int(mind_id))
            if mind_data:
                minds.append(mind_data)
        
        return JsonResponse({
            'minds': minds,
            'count': len(minds)
        }, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def upsert_mind(request):
    try:
        data = get_request_data(request)
        
        mind_id = data.get('id')
        mind_name = data.get('name', '').strip()
        detail = data.get('detail', '').strip()
        color = data.get('color', '#FFFFFF')
        rec_status = data.get('rec_status', True)
        position = data.get('position', [0, 0, 0])
        rotation = data.get('rotation', [0, 0, 0])
        scale = data.get('scale', 1.0)
        
        if not mind_name:
            return JsonResponse({'error': 'name is required'}, status=400)
        
        if not isinstance(position, list) or len(position) != 3:
            return JsonResponse({'error': 'position must be an array of 3 floats [x, y, z]'}, status=400)
        
        if not isinstance(rotation, list) or len(rotation) != 3:
            return JsonResponse({'error': 'rotation must be an array of 3 floats [x, y, z]'}, status=400)
        
        _, root = get_connection()
        
        mind_data = {
            'name': mind_name,
            'detail': detail,
            'color': color,
            'rec_status': rec_status,
            'position': position,
            'rotation': rotation,
            'scale': scale,
            'created_by': request.user.id
        }
        
        if mind_id:
            updated_mind_id = update_mind_zodb(root, int(mind_id), mind_data)
        else:
            updated_mind_id = create_mind_zodb(root, mind_data)
        
        # Get the updated/created mind
        mind = get_mind_zodb(root, updated_mind_id)
        
        return JsonResponse({
            'message': 'Mind saved successfully',
            'mind': mind
        }, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def add_mental_sphere(request):
    """
    Add MentalSpheres to a Mind
    POST body: {
        "mind_id": int,
        "sphere_id": [1, 2, 3]
    }
    Returns: { "mental_spheres": [...] }
    """
    try:
        data = get_request_data(request)
        
        mind_id = data.get('mind_id')
        sphere_ids = data.get('sphere_id', [])
        
        if not mind_id:
            return JsonResponse({'error': 'mind_id is required'}, status=400)
        
        if not isinstance(sphere_ids, list):
            return JsonResponse({'error': 'sphere_id must be an array'}, status=400)
        
        _, root = get_connection()
        
        # Add spheres to mind
        add_mental_spheres_to_mind(root, int(mind_id), sphere_ids)
        
        # Get the mental spheres
        spheres = []
        for sphere_id in sphere_ids:
            sphere_data = get_mental_sphere_zodb(root, int(sphere_id))
            if sphere_data:
                spheres.append(sphere_data)
        
        return JsonResponse({
            'message': 'Mental spheres added successfully',
            'mental_spheres': spheres
        }, status=200)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def delete_mental_sphere(request):
    """
    Remove MentalSpheres from a Mind
    POST body: {
        "mind_id": int,
        "sphere_id": [1, 2, 3]
    }
    Returns: { "mental_spheres": [...] }
    """
    try:
        data = get_request_data(request)
        
        mind_id = data.get('mind_id')
        sphere_ids = data.get('sphere_id', [])
        
        if not mind_id:
            return JsonResponse({'error': 'mind_id is required'}, status=400)
        
        if not isinstance(sphere_ids, list):
            return JsonResponse({'error': 'sphere_id must be an array'}, status=400)
        
        _, root = get_connection()
        
        # Remove spheres from mind
        delete_mental_spheres_from_mind(root, int(mind_id), sphere_ids)
        
        # Get the removed mental spheres info
        spheres = []
        for sphere_id in sphere_ids:
            sphere_data = get_mental_sphere_zodb(root, int(sphere_id))
            if sphere_data:
                spheres.append(sphere_data)
        
        return JsonResponse({
            'message': 'Mental spheres removed successfully',
            'mental_spheres': spheres
        }, status=200)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============= MentalSphere CRUD Methods =============

@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def create_sphere(request):
    try:
        data = get_request_data(request)
        _, root = get_connection()
        
        sphere_data = {
            'name': data.get('name', ''),
            'detail': data.get('detail', ''),
            'color': data.get('color', '#FFFFFF'),
            'image': data.get('image', ''),
            'rec_status': data.get('rec_status', True),
            'position': data.get('position', [0, 0, 0]),
            'rotation': data.get('rotation', [0, 0, 0]),
            'scale': data.get('scale', 1.0),
            'created_by': request.user.id
        }
        
        sphere_id = create_mental_sphere_zodb(root, sphere_data)
        sphere = get_mental_sphere_zodb(root, sphere_id)
        
        return JsonResponse({
            'message': 'Mental sphere created successfully',
            'mental_sphere': sphere
        }, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
@require_auth
def list_spheres(request):
    """Get all mental spheres for the current user"""
    try:
        _, root = get_connection()
        
        if not hasattr(root, 'mentalSpheres'):
            return JsonResponse({'mental_spheres': [], 'count': 0}, status=200)
        
        spheres = []
        for sphere_id, sphere_obj in root.mentalSpheres.items():
            if sphere_obj.get_created_by_id() == request.user.id:
                sphere_data = get_mental_sphere_zodb(root, int(sphere_id))
                if sphere_data:
                    spheres.append(sphere_data)
        
        return JsonResponse({
            'mental_spheres': spheres,
            'count': len(spheres)
        }, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
@require_auth
def get_sphere(request, sphere_id):
    """Get a specific mental sphere by ID"""
    try:
        _, root = get_connection()
        sphere = get_mental_sphere_zodb(root, sphere_id)
        
        if not sphere:
            return JsonResponse({'error': 'Mental sphere not found'}, status=404)
        
        # Check if user owns this sphere
        if sphere['created_by_id'] != request.user.id:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        return JsonResponse({'mental_sphere': sphere}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def update_sphere(request, sphere_id):
    """Update a mental sphere"""
    try:
        _, root = get_connection()
        
        # Check if sphere exists and user owns it
        existing_sphere = get_mental_sphere_zodb(root, sphere_id)
        if not existing_sphere:
            return JsonResponse({'error': 'Mental sphere not found'}, status=404)
        
        if existing_sphere['created_by_id'] != request.user.id:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        data = get_request_data(request)
        update_mental_sphere_zodb(root, sphere_id, data)
        
        # Get updated sphere
        sphere = get_mental_sphere_zodb(root, sphere_id)
        
        return JsonResponse({
            'message': 'Mental sphere updated successfully',
            'mental_sphere': sphere
        }, status=200)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
@require_auth
def delete_sphere(request, sphere_id):
    """Delete a mental sphere"""
    try:
        _, root = get_connection()
        
        # Check if sphere exists and user owns it
        existing_sphere = get_mental_sphere_zodb(root, sphere_id)
        if not existing_sphere:
            return JsonResponse({'error': 'Mental sphere not found'}, status=404)
        
        if existing_sphere['created_by_id'] != request.user.id:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        delete_mental_sphere_zodb(root, sphere_id)
        
        return JsonResponse({'message': 'Mental sphere deleted successfully'}, status=200)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
