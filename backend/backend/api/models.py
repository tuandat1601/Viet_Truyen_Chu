from django.db import models
from django.conf import settings
# Create your models here.
class AuthorStory(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=20)

class TypeStory(models.Model):
    typename = models.CharField(max_length=50)
class LongStory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField()
    isPublish = models.BooleanField(False)
    type = models.CharField(max_length=100)
    author_id = models.ForeignKey(AuthorStory,on_delete=models.CASCADE)
    class Meta:
        db_table="LongStory"
class ChapterSotry(models.Model):
    chapter = models.IntegerField()
    name = models.CharField(max_length=100)
    content = models.TextField()
    isPublish = models.BooleanField(False)

    story_id = models.ForeignKey(LongStory,on_delete=models.CASCADE)
    class Meta:
        db_table = "StoryChapter"
class Comment(models.Model):
    storyid = models.ForeignKey(ChapterSotry, on_delete=models.CASCADE)
    author = models.ForeignKey(AuthorStory, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)