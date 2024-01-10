# models.py

from django.db import models

gender = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ]

class User(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=gender)
    country = models.CharField(max_length=50)
    is_online = models.BooleanField(default=False)
    interests = models.ManyToManyField('Interest', related_name='users', blank=True)

class Interest(models.Model):
    name = models.CharField(max_length=50, unique=True)

class ChatSave(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
