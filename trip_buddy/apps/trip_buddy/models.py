from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 100)
    password = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Trip(models.Model):
    name = models.CharField(max_length = 255)
    start = models.DateField()
    end = models.DateField()
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    travelers = models.ManyToManyField(User, related_name='trips')
    planned_by = models.ForeignKey(User, related_name='planned_trip', on_delete=models.CASCADE)