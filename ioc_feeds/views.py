from django.shortcuts import render
from rest_framework import viewsets

from ioc_feeds.models import Ioc
from ioc_feeds.serializers import IoCSerializer
from rest_framework.response import Response 

# Create your views here.
class IocViewSet(viewsets.ViewSet):
    def list(self, request):
        iocs = Ioc.objects.all()
        print(iocs)
        serializer = IoCSerializer(iocs, many=True)
        print(serializer)
        return Response(serializer.data)



