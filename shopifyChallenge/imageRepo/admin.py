from django.contrib import admin
from .models import Image, Directory, Media, Video, Node

# Register your models here.
admin.site.register(Image)
admin.site.register(Directory)
admin.site.register(Media)
admin.site.register(Video)
admin.site.register(Node)
