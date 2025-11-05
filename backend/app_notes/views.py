import json
from functools import wraps
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .models import Note


def get_request_data(request):
    """Helper to get data from JSON or form-data"""
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


@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def create_note(request):
    """Create a new note"""
    data = get_request_data(request)
    
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    
    if not title:
        return JsonResponse({'error': 'title is required'}, status=400)
    
    try:
        with transaction.atomic():
            note = Note.objects.create(
                title=title,
                content=content,
                user=request.user
            )
        
        return JsonResponse({
            'message': 'Note created successfully',
            'note': {
                'id': note.id,
                'title': note.title,
                'content': note.content,
                'created_at': note.created_at.isoformat(),
                'updated_at': note.updated_at.isoformat(),
                'is_archived': note.is_archived
            }
        }, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
@require_auth
def list_notes(request):
    """Get all notes for the current user"""
    try:
        archived = request.GET.get('archived', 'false').lower() == 'true'
        notes = Note.objects.filter(user=request.user, is_archived=archived)
        
        notes_list = [{
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'created_at': note.created_at.isoformat(),
            'updated_at': note.updated_at.isoformat(),
            'is_archived': note.is_archived
        } for note in notes]
        
        return JsonResponse({
            'notes': notes_list,
            'count': len(notes_list)
        }, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
@require_auth
def get_note(request, note_id):
    """Get a specific note by ID"""
    try:
        note = Note.objects.get(id=note_id, user=request.user)
        return JsonResponse({
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'created_at': note.created_at.isoformat(),
            'updated_at': note.updated_at.isoformat(),
            'is_archived': note.is_archived
        }, status=200)
    except Note.DoesNotExist:
        return JsonResponse({'error': 'Note not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
@require_auth
def update_note(request, note_id):
    """Update a note"""
    try:
        note = Note.objects.get(id=note_id, user=request.user)
        data = get_request_data(request)
        
        if 'title' in data:
            note.title = data.get('title', '').strip()
        if 'content' in data:
            note.content = data.get('content', '').strip()
        if 'is_archived' in data:
            note.is_archived = data.get('is_archived', False)
        
        if not note.title:
            return JsonResponse({'error': 'title cannot be empty'}, status=400)
        
        note.save()
        
        return JsonResponse({
            'message': 'Note updated successfully',
            'note': {
                'id': note.id,
                'title': note.title,
                'content': note.content,
                'created_at': note.created_at.isoformat(),
                'updated_at': note.updated_at.isoformat(),
                'is_archived': note.is_archived
            }
        }, status=200)
    except Note.DoesNotExist:
        return JsonResponse({'error': 'Note not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
@require_auth
def delete_note(request, note_id):
    """Delete a note"""
    try:
        note = Note.objects.get(id=note_id, user=request.user)
        note.delete()
        return JsonResponse({'message': 'Note deleted successfully'}, status=200)
    except Note.DoesNotExist:
        return JsonResponse({'error': 'Note not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
