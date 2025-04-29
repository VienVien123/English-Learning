from django.db import models
from django.contrib.auth.models import User

# Chủ đề hệ thống (backup)
class Topic(models.Model):

    topic= models.CharField(max_length=100)
    english= models.CharField(max_length=100, blank=True, null=True)  # Từ tiếng Anh
    ipa= models.CharField(max_length=100, blank=True, null=True)  # Phiên âm IPA
    type= models.CharField(max_length=100, blank=True, null=True)  # Loại từ (danh từ, động từ, tính từ...)
    vietnamese= models.CharField(max_length=100, blank=True, null=True)  # Nghĩa tiếng Việt
    synced = models.BooleanField(default=True)  # ✅ đã đồng bộ với Supabase chưa

    def __str__(self):
        return self.name

# Từ vựng người dùng (backup)
class Word(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    definition = models.TextField(blank=True)
    example = models.TextField(blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    is_learned = models.BooleanField(default=False)
    synced = models.BooleanField(default=True)  # ✅ đã sync với Supabase chưa
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.word


