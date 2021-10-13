from rest_framework import viewsets, status
from .serializers import imageSerializer, directorySerializer, videoSerializer, nodeSerializer
from .models import Image, Directory, Video, Node
from datetime import datetime
from rest_framework.response import Response
from tensorflow.keras.models import load_model
import cv2
import numpy
import uuid
import numpy as np
import pandas as pd
from django.conf import settings
import os
import json

def imageHash(image, size=8):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (size + 1, size))

    diff = img[:, 1:] > img[:, :-1]
    diff = diff.flatten().astype(int)
    return "".join(str(x) for x in diff)


def hammingDistance(n1, n2):
    n1 = int(n1, 2)
    n2 = int(n2, 2)
    x = n1 ^ n2
    setBits = 0
    while (x > 0):
        setBits += x & 1
        x >>= 1
    return setBits

class nodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = nodeSerializer

    def validate(self, nodeId, parentId):
        return len(Directory.objects.filter(id=parentId)) == 1

    def updateModified(self, directoryId):
        parent = Directory.objects.get(id=directoryId).parent
        Directory.objects.filter(id=directoryId).update(modified=datetime.now())
        if directoryId != '1':
            self.updateModified(parent.id)

    def executeUpdate(self, nodeId, parentId):
        self.queryset.filter(id=nodeId).update(parent=parentId)
        self.updateModified(parentId)

    def update(self, request, *args, **kwargs):
        self.queryset = Node.objects.all()
        nodeId = request.POST['id']
        parentId = request.POST['parentId']

        if self.validate(nodeId, parentId) and nodeId != '1':
            self.executeUpdate(nodeId, parentId)
            return Response({'result': 'ok'})
        else:
            return Response({'result': 'no'}, status=status.HTTP_400_BAD_REQUEST)

class directoryViewSet(nodeViewSet):
    queryset = Directory.objects.all().order_by('modified')
    serializer_class = directorySerializer

    def list(self, request, *args, **kwargs):
        self.queryset = Directory.objects.all().order_by('name').reverse()
        parentId = request.GET.get('parentId', None)
        result = self.queryset

        if parentId:
            parent = self.queryset.get(id=parentId)
            result = result.filter(parent=parent)

        return Response([self.serializer_class(i).data for i in result])

    def validate(self, nodeId, parentId):
        return len(Directory.objects.filter(id=parentId)) == 1 and len(Directory.objects.filter(id=nodeId)) == 1


    def executeUpdate(self, nodeId, parentId):
        parent = Directory.objects.get(id=parentId)
        directory = Directory.objects.get(id=nodeId)
        samePath = Directory.objects.filter(parent=parent).filter(name=directory.name)
        if (len(samePath) > 0):
            Node.objects.filter(parent=directory).update(parent=samePath[0])
            Directory.objects.filter(id=nodeId).delete()
        else:
            Directory.objects.filter(id=nodeId).update(parent=parentId)
        self.updateModified(parentId)

    def create(self, request, *args, **kwargs):
        self.queryset = Directory.objects.all().order_by('modified')
        parent = self.queryset.get(id=request.POST['parentId'])
        name = request.POST['name']
        sameNameChildren = self.queryset.filter(name=name).filter(parent=parent)

        if len(sameNameChildren) == 0:
            Directory.objects.create(id=str(uuid.uuid4()), name=name, parent=parent)
            return Response({'result': 'ok'})
        else:
            return Response({'result': 'no'}, status=status.HTTP_400_BAD_REQUEST)

class videoViewSet(nodeViewSet):
    queryset = Video.objects.all().order_by('created').reverse()
    serializer_class = videoSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = Video.objects.all().order_by('created').reverse()
        parentId = request.GET.get('parentId', None)
        result = self.queryset
        if parentId:
            parent = Directory.objects.get(id=parentId)
            result = result.filter(parent=parent)

        return Response([self.serializer_class(i).data for i in result])

    def create(self, request, *args, **kwargs):
        self.queryset = Video.objects.all().order_by('created').reverse()
        vid = request.FILES['main_file']

        Video.objects.create(
            id=str(uuid.uuid4()), title=request.POST['title'], main_file=vid)
        return Response({'result':'ok'})

class imageViewSet(nodeViewSet):
    queryset = Image.objects.all().order_by('created').reverse()
    serializer_class = imageSerializer

    def classifyContent(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (200, 200))
        img = cv2.normalize(img, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

        testData = np.array([img])
        testData = np.array([x.reshape(200, 200, 1) for x in testData])

        model = load_model(os.path.join(settings.CLASSIFIER_ROOT, 'models/model1_10000_literer'))
        predictions = model.predict(testData)

        data = pd.read_csv(os.path.join(settings.CLASSIFIER_ROOT, 'data/classMappingLiterer.csv'))
        classes = []
        for i in range(len(predictions[0])):
            if (predictions[0][i] > 0.45):
                classes.append(data['Word'][i])
        return classes

    def list(self, request, *args, **kwargs):
        self.queryset = Image.objects.all().order_by('created').reverse()
        parentId = request.GET.get('parentId', None)
        contentFilters = json.loads(request.GET.get('content', '[]'))
        result = self.queryset
        if parentId:
            parent = Directory.objects.get(id=parentId)
            result = result.filter(parent=parent)
        if len(contentFilters) > 0:
            filtered = []
            for i in result:
                content = i.content
                if('content' in content):
                    if bool(set(content['content']) & set(contentFilters)):
                        filtered.append(self.serializer_class(i).data)
            return Response(filtered)
        else:
            return Response([self.serializer_class(i).data for i in result])

    def create(self, request, *args, **kwargs):
        self.queryset = Image.objects.all().order_by('created').reverse()
        img = request.FILES['main_file']
        decodedImg = cv2.imdecode(numpy.fromstring(img.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)

        content = self.classifyContent(decodedImg);

        Image.objects.create(
            id=str(uuid.uuid4()), title=request.POST['title'], hash=imageHash(decodedImg), main_file=img, width=decodedImg.shape[1], height=decodedImg.shape[0], content={'content':content})
        return Response({'result':'ok'})

class imageSearchViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all().order_by('created').reverse()
    serializer_class = imageSerializer

    def create(self, request, *args, **kwargs):
        self.queryset = Image.objects.all().order_by('created').reverse()
        img = cv2.imdecode(numpy.fromstring(request.FILES['main_file'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
        hash = imageHash(img)
        hits = []
        for i in self.queryset:
            if(hammingDistance(hash, i.hash) <= 10):
                hits.append(self.serializer_class(i).data)

        return Response(hits)

