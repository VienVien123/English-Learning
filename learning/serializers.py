from rest_framework import serializers
from .models import Topic, Word

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = [
            'id', 'user', 'word', 'definition', 'example',
            'topic', 'is_learned', 'synced', 'created_at', 'updated_at'
        ]

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fileds=['id','topic','english','ipa','type','vietnamese']
        # fields = ['id', 'name', 'definition', 'example', 'category', 'synced']
