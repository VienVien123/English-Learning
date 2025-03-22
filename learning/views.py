from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django import forms

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
    topics_list = [
        {
            'title': 'Travel',
            'description': 'Learn essential phrases for your next adventure.',
            'image': 'https://source.unsplash.com/random/800x600?travel',
            'level': 'Beginner'
        },
        {
            'title': 'Business',
            'description': 'Master professional English communication.',
            'image': 'https://source.unsplash.com/random/800x600?business',
            'level': 'Intermediate'
        },
        {
            'title': 'Daily Life',
            'description': 'Practice everyday conversations and situations.',
            'image': 'https://source.unsplash.com/random/800x600?conversation',
            'level': 'Beginner'
        },
        {
            'title': 'Academic',
            'description': 'Improve your academic English skills.',
            'image': 'https://source.unsplash.com/random/800x600?university',
            'level': 'Advanced'
        },
        {
            'title': 'Technology',
            'description': 'Learn tech-related vocabulary and expressions.',
            'image': 'https://source.unsplash.com/random/800x600?technology',
            'level': 'Intermediate'
        },
        {
            'title': 'Culture',
            'description': 'Explore cultural aspects of English-speaking countries.',
            'image': 'https://source.unsplash.com/random/800x600?culture',
            'level': 'Intermediate'
        }
    ]
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
