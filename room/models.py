from django.db import models
from accounts.models import Account

# Create your models here.
class Room(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    creador = models.CharField(max_length=100)
    invitado = models.CharField(max_length=100)

    def __str__(self):
        return self.creador

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)