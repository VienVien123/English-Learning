from rest_framework import serializers
from rest_framework.permissions import AllowAny
from .models import Topic, Word

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'word', 'definition', 'example', 'category', 'is_learned']

class TopicSerializer(serializers.ModelSerializer):
     words = WordSerializer(many=True, read_only=True)
     class Meta:
        model = Topic
        fields = ['id', 'wordt', 'definition', 'example', 'category','words' ]
