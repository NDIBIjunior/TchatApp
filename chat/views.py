from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from django.http import JsonResponse
import uuid

def index(request):
    # Page de saisie du nom et du salon
    return render(request, "chat/index.html")

def test_ui(request):
    # Page de test de l'interface utilisateur
    return render(request, "chat/reserve.html")

def room(request, room_name, user_name):
    # Affiche la salle de chat, transmet le nom de la salle
    return render(request, "chat/room.html", {
        "room_name": room_name,
        "user_name":user_name
    })


@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        save_dir = settings.MEDIA_ROOT
        os.makedirs(save_dir, exist_ok=True)
        ext = os.path.splitext(uploaded_file.name)[1]
        unique_filename = str(uuid.uuid4()) + ext
        file_path = os.path.join(save_dir, unique_filename)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        file_url = os.path.join(settings.MEDIA_URL, unique_filename)
        return JsonResponse({'file_url': file_url, 'original_name': uploaded_file.name})
    return JsonResponse({'error': 'Invalid request'}, status=400)
