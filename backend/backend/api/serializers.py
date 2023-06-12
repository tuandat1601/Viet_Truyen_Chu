from rest_framework import serializers
from .models import User, LongStory,TypeStory,Story
image_path = "media/kem.jpg"
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
      

    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     return user
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class LongStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LongStory
        fields = ('name', 'description', 'image', 'isPublish','type','author_id')
class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ('name', 'description', 'image', 'isPublish','type','author_id')
    # def validate_image(self, value):
    #     if not value:
    #         # Gán hình ảnh mặc định
    #         value = 'backend/backend/media/kem.png'  # Đường dẫn tới hình ảnh mặc định
    #     return value
    def getData(self,obj):
        return f"{obj.name} {obj.description}"

class TypeStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeStory
        fields = ('id','typename')
   
     
