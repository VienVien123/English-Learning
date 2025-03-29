from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Topic, Word
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Word
from .serializers import WorkSerializer

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
def add_word(request):
    if request.method == 'POST':
        word = request.POST.get('word')
        definition = request.POST.get('definition')
        example = request.POST.get('example')
        topic_id = request.POST.get('topic')
        topic = Topic.objects.get(id=topic_id)
        Word.objects.create(word=word, definition=definition, example=example, topic=topic, user=request.user)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

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
