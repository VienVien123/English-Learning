from django.urls import path
from . import views


urlpatterns = [
    # Giao diện
    path('', views.home, name='home'),
    path('vocabulary/', views.vocabulary, name='vocabulary'),

    # Từ của user (gọi Supabase)
    path('api/user-words/', views.get_user_words, name='get_user_words'),
    path('api/user-words/add/', views.add_user_word, name='add_user_word'),
    path('api/user-words/edit/<int:word_id>/', views.edit_user_word, name='edit_user_word'),
    path('api/user-words/delete/<int:word_id>/', views.delete_user_word, name='delete_user_word'),

    # Từ hệ thống
    path('api/topics/', views.get_topics, name='get_topics'),
    path('api/vocabulary/<str:topic_name>/', views.get_vocabulary_by_topic, name='get_vocabulary_by_topic'),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
     path('topics/', views.topics, name='topics'),
]
