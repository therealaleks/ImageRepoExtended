from django.db import models
from datetime import datetime
from django.dispatch import receiver
import os

class Node(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    parent = models.ForeignKey('Directory', on_delete=models.CASCADE, default='1')
class Directory(Node):
    name = models.CharField(max_length=100)
    modified = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.name

class Media(Node):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(default=datetime.now)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Video(Media):
    length = models.IntegerField(default=0)
    main_file = models.FileField(upload_to='videos/', default='video/default.jpg')

class Image(Media):
    hash = models.TextField(max_length=64)
    main_file = models.ImageField(upload_to='images/', default='images/default.jpg')
    content = models.JSONField(default=dict)


@receiver(models.signals.post_delete, sender=Image)
@receiver(models.signals.post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.main_file:
        if os.path.isfile(instance.main_file.path):
            os.remove(instance.main_file.path)