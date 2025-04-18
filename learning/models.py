from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    wordt = models.CharField(max_length=100)
    definition = models.TextField(blank=True)
    example = models.TextField(null=True,blank=True)
    category = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.wordt

    class Meta:
        ordering = ['wordt']

class Word(models.Model):
    # name = models.CharField(max_length=100, default='Default Topic')
    word = models.CharField(max_length=100)
    definition = models.TextField(blank=True)
    example = models.TextField(blank=True)
    category = models.CharField(max_length=100,null=True, blank=True)

    # topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='words')

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_learned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.word

