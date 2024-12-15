from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, 
        on_delete=models.CASCADE)
    name = models.CharField(max_length=50, 
        blank=True, null=True)
    email = models.EmailField(max_length=50, 
        blank=True, null=True)
    username = models.CharField(max_length=50, 
        blank=True, null=True)

    class Meta:
        ordering = ['created']
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username

class Message(models.Model):
    sender = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL, 
        null=True,
        blank=True
    )
    recipient = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='messages'
        )
    name = models.CharField(
        max_length=200, 
        null=True,
        blank=True
    )
    email = models.EmailField(
        max_length=200, 
        null=True,
        blank=True
    )
    subject = models.CharField(
        max_length=200, 
        null=True,
        blank=True
    )
    body = models.TextField()
    is_read = models.BooleanField(
        default=False,
        null=True
    )
    created = models.DateTimeField(auto_now_add=True)