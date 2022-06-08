from django.db import models

# Create your models here.
class Room(models.Model):
    room = models.CharField(max_length=200, default='no')
    content = models.TextField(default='<svg></svg>')

    def publish(self):
        self.save()

    def __str__(self):
        return self.name