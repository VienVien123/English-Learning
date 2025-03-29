from rest_framework import serializers
from .models import Topic, Word

class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'word', 'definition', 'example', 'topic', 'is_learned']

class TopicSerializer(serializers.ModelSerializer):
    words = WorkSerializer(many=True, read_only=True)
    
    class Meta:
        model = Topic
        fields = ['id', 'name', 'description', 'words']
