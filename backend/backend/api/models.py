from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError("Username is required.")
        if not email:
            raise ValueError("Email address is required.")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

class TypeStory(models.Model):
    typename = models.CharField(max_length=50)
Users = get_user_model()
class LongStory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField()
    isPublish = models.BooleanField(False)
    type = models.CharField(max_length=100)
    author_id = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        db_table="LongStory"
class Story(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField()
    isPublish = models.BooleanField(False)
    type = models.CharField(max_length=100)
    author_id = models.ForeignKey(Users,on_delete=models.CASCADE)
    class Meta:
        db_table="Story"
class ChapterSotry(models.Model):
    chapter = models.IntegerField()
    name = models.CharField(max_length=100)
    content = models.TextField()
    isPublish = models.BooleanField(False)

    story_id = models.ForeignKey(Story,on_delete=models.CASCADE)
    class Meta:
        db_table = "StoryChapter"
class Comment(models.Model):
    storyid = models.ForeignKey(ChapterSotry, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)