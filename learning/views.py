import os, json, requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Word, Topic
from django.views.decorators.csrf import csrf_exempt
import requests, json, os
import environ
from dotenv import load_dotenv
env = environ.Env()
environ.Env.read_env()
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Topic, Word
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Word
from .serializers import WordSerializer, TopicSerializer
from django.views.decorators.http import require_http_methods
import json
load_dotenv()

SUPABASE_URL = env("SUPABASE_URL")
SUPABASE_API_KEY = env("SUPABASE_API_KEY")

HEADERS = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

# ------------------ Web Pages ------------------
def topics(request):
    topics_list = Topic.objects.all()

    return render(request, 'topics.html', {'topics': topics_list})
def home(request):
    return render(request, 'home.html')

from django.conf import settings

def vocabulary(request):
    vocab = Word.objects.all()
    return render(request, 'vocabulary.html', {
        "SUPABASE_URL": settings.SUPABASE_URL,
        "SUPABASE_API_KEY": settings.SUPABASE_API_KEY,
        "USER_ID": request.user.id if request.user.is_authenticated else None
    })
# ------------------ API: USER WORDS ------------------

@login_required
@csrf_exempt
@require_http_methods(["GET"])
def get_user_words(request):
    url = f"{SUPABASE_URL}/rest/v1/user_words?user_id=eq.{request.user.id}&select=*"
    r = requests.get(url, headers=HEADERS)
    return JsonResponse(r.json(), safe=False, status=r.status_code)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def add_user_word(request):
    data = json.loads(request.body)
    payload = {
        "user_id": request.user.id,
        "word": data["word"],
        "definition": data.get("definition", ""),
        "example": data.get("example", ""),
        "topic": data.get("topic", ""),
        "is_learned": False
    }
    r = requests.post(f"{SUPABASE_URL}/rest/v1/user_words", headers=HEADERS, json=payload)
    return JsonResponse(r.json(), safe=False, status=r.status_code)

@login_required
@csrf_exempt
@require_http_methods(["PUT"])
def edit_user_word(request, word_id):
    data = json.loads(request.body)
    payload = {
        "word": data.get("word"),
        "definition": data.get("definition"),
        "example": data.get("example"),
        "topic": data.get("topic"),
        "is_learned": data.get("is_learned", False)
    }
    url = f"{SUPABASE_URL}/rest/v1/user_words?id=eq.{word_id}&user_id=eq.{request.user.id}"
    r = requests.patch(url, headers=HEADERS, json=payload)
    return JsonResponse({"status": "updated"} if r.status_code == 204 else r.text, status=r.status_code)

@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_user_word(request, word_id):
    url = f"{SUPABASE_URL}/rest/v1/user_words?id=eq.{word_id}&user_id=eq.{request.user.id}"
    r = requests.delete(url, headers=HEADERS)
    return JsonResponse({"status": "deleted"} if r.status_code == 204 else r.text, status=r.status_code)

# ------------------ API: SYSTEM DATA (TOPICS & VOCABULARY) ------------------

@csrf_exempt
@require_http_methods(["GET"])
def get_topics(request):
    url = f"{SUPABASE_URL}/rest/v1/topics?select=*"
    r = requests.get(url, headers=HEADERS)
    return JsonResponse(r.json(), safe=False, status=r.status_code)

@csrf_exempt
@require_http_methods(["GET"])
def get_vocabulary_by_topic(request, topic_name):
    url = f"{SUPABASE_URL}/rest/v1/vocabulary?topic=eq.{topic_name}&select=english,vietnamese,ipa,type"
    r = requests.get(url, headers=HEADERS)
    return JsonResponse(r.json(), safe=False, status=r.status_code)
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('home')
    return render(request, 'login.html')
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = UserCreationForm.Meta.model
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
            # return JsonResponse({'status': 'success', 'message': 'Account created successfully!'})
        else:
            errors = {field: str(error[0]) for field, error in form.errors.items()}
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('home')
    # return JsonResponse({'status': 'success', 'message': 'Successfully logged out!'})
