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

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = UserCreationForm.Meta.model
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

def home(request):
    return render(request, 'home.html')

def topics(request):
    topics_list = Topic.objects.all()
    return render(request, 'topics.html', {'topics': topics_list})

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
    return render(request, 'login.html')

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
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('home')

def vocabulary(request):
    topics = Topic.objects.all()
    words = Word.objects.all()
    if request.user.is_authenticated:
        words = Word.objects.filter(user=request.user)
    return render(request, 'vocabulary.html', {'topics': topics, 'words': words})

@login_required
def add_topic(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        Topic.objects.create(name=name, description=description, user=request.user)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def get_topics(request):
    topics = Topic.objects.all()
    topics_data = [{'id': topic.id, 'name': topic.name} for topic in topics]
    return JsonResponse(topics_data, safe=False)

@login_required
def get_words(request):
    words = Word.objects.filter(user=request.user)
    words_data = [{
        'id': word.id,
        'word': word.word,
        'definition': word.definition,
        'example': word.example,
        'topic': word.topic.id if word.topic else None,
        'topic_name': word.topic.name if word.topic else None,
        'is_learned': word.is_learned
    } for word in words]
    return JsonResponse(words_data, safe=False)

@login_required
@require_http_methods(['POST'])
def add_word(request):
    try:
        data = json.loads(request.body)
        # Create word object
        word = Word.objects.create(
            user=request.user,
            word=data['word'],
            definition=data['definition'],
            example=data.get('example', ''),
            topic=Topic.objects.get(id=data['topic']) if data.get('topic') else None
        )
        
        # Return word data
        return JsonResponse({
            'id': word.id,
            'word': word.word,
            'definition': word.definition,
            'example': word.example,
            'topic': word.topic.id if word.topic else None,
            'topic_name': word.topic.name if word.topic else None,
            'is_learned': word.is_learned
        })
    except Topic.DoesNotExist:
        return JsonResponse({'error': 'Topic not found'}, status=400)
    except Exception as e:
        print(f"Error adding word: {str(e)}")  # Debug log
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def edit_word(request, word_id):
    word = get_object_or_404(Word, id=word_id, user=request.user)
    if request.method == 'POST':
        word.word = request.POST.get('word')
        word.definition = request.POST.get('definition')
        word.example = request.POST.get('example')
        word.topic_id = request.POST.get('topic')
        word.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def delete_word(request, word_id):
    word = get_object_or_404(Word, id=word_id, user=request.user)
    if request.method == 'POST':
        word.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def mark_word_learned(request, word_id):
    word = get_object_or_404(Word, id=word_id, user=request.user)
    if request.method == 'POST':
        word.is_learned = not word.is_learned
        word.save()
        return JsonResponse({'status': 'success', 'is_learned': word.is_learned})
    return JsonResponse({'status': 'error'}, status=400)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# API CRUD
class TopicViewSet(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [AllowAny]  # Ai cũng có thể xem chủ đề

    def get_queryset(self):
        return Topic.objects.all()
    
class WordViewSet(ModelViewSet):
    serializer_class = WordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Word.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
