from rest_framework import serializers
from .models import Image, Directory, Video, Media, Node

class imageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ['title', 'main_file', 'content', 'id']

class directorySerializer(serializers.HyperlinkedModelSerializer):
    parentId = serializers.CharField(source='parent.id', allow_null=True)
    class Meta:
        model = Directory
        fields = ['id', 'name', 'modified', 'parentId']

class videoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'created', 'main_file']

class mediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'created', 'title']

class nodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Node
        fields = ['id']