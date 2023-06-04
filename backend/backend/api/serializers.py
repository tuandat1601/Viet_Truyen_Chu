from rest_framework import serializers
from .models import AuthorStory
class AuthorStorySerializers(serializers.ModelSerializer):
    class Meta:
        model = AuthorStory
        fields=["id","name","email"]
