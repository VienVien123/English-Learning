from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TopicViewSet, WordViewSet

router = DefaultRouter()
router.register(r'topics', views.TopicViewSet,basename='topics')
router.register(r'words', views.WordViewSet,basename='words')

urlpatterns = [
    # api
    path('api/', include(router.urls)),
    path('api/auth/status/', views.check_auth_status, name='check_auth_status'),
    # web
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('topics/', views.topics, name='topics'),
    path('vocabulary/', views.vocabulary, name='vocabulary'),
    path('vocabulary/add-topic/', views.add_topic, name='add_topic'),
    path('vocabulary/add-word/', views.add_word, name='add_word'),
    path('vocabulary/edit-word/<int:word_id>/', views.edit_word, name='edit_word'),
    path('vocabulary/delete-word/<int:word_id>/', views.delete_word, name='delete_word'),
    path('vocabulary/mark-word-learned/<int:word_id>/', views.mark_word_learned, name='mark_word_learned'),
] 