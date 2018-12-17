from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 100)
    password = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Quote(models.Model):
    author = models.CharField(max_length = 255)
    quote = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    posted_by = models.ForeignKey(User, related_name='posted_quote', on_delete=models.CASCADE)

