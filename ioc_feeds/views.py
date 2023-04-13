"""
This is our API which will basically be to query our IOCS
"""

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from ioc_feeds.models import Ioc, IndicatorType, Stats
from ioc_feeds.serializers import IoCSerializer
from ioc_feeds.pagination import IoCViewSetPagination

import ioc_feeds.consts

import datetime

# Create your views here.
# This view gets all the iocs!
class IocViewSet(viewsets.ViewSet):
    # get all IOCS!
    def list(self, request):
        iocs = Ioc.objects.all()
        paginator = IoCViewSetPagination()
        paginated_iocs = paginator.paginate_queryset(iocs, request)
        serializer = IoCSerializer(paginated_iocs, many=True)
        return paginator.get_paginated_response(serializer.data)


# This view gets all the iocs from a specifec source!
class SourceIocViewSet(viewsets.ViewSet):

    @action(detail=False, methods=["GET"])
    def count(self, request):
        count = {}
        for source in ioc_feeds.consts.sources:
            source_count = Ioc.objects.filter(sources__contains=source).count()
            count[source] = source_count

        return Response(count) 

    # helper function to get all the iocs from a specific source!
    def __get_iocs_from_source(self, source):
        print(f"getting iocs from source {source}")
        iocs = Ioc.objects.filter(sources__contains=source)
        return iocs

    def get(self, request, source):
        iocs = self.__get_iocs_from_source(source)        
        paginator = IoCViewSetPagination()
        paginated_iocs = paginator.paginate_queryset(iocs, request)
        serializer = IoCSerializer(paginated_iocs, many=True)
        return paginator.get_paginated_response(serializer.data)
    

# This view gets all the iocs from a date i.e less than equal to day, month, year! 
"""
url parameters:
    1. day -> defaults to 1
    2. month -> defaults to 1
    3. year -> defaults to 1
"""
class DateIocViewSet(viewsets.ViewSet):
    def get(self, request):
        day = int(request.GET.get("day", 1))
        month = int(request.GET.get("month", 1))
        year = int(request.GET.get("year", 1))
        print(f"Day: {day} | Month: {month} | Year: {year}")
        iocs = Ioc.objects.filter(created_timestamp__lte=datetime.date(year, month, day))
        serializer = IoCSerializer(iocs, many=True)
        print(serializer)
        return Response(serializer.data)

# This view gets all the iocs of a particular IOC type
class IocTypeViewSet(viewsets.ViewSet):

    @action(detail=False, methods=["GET"])
    def count(self, request):
        count = {}
        for indicator_type in IndicatorType:
            iocs_count = Ioc.objects.filter(type=indicator_type).count()
            count[indicator_type.name] = iocs_count
        return Response(count)

    def get(self, request, ioc_type):
        indicator_type = IndicatorType[ioc_type]
        iocs = Ioc.objects.filter(type=indicator_type)
        paginator = IoCViewSetPagination()
        paginated_iocs = paginator.paginate_queryset(iocs, request)
        serializer = IoCSerializer(paginated_iocs, many=True)
        return paginator.get_paginated_response(serializer.data)

class StatsViewSet(viewsets.ViewSet):

    @action(detail=False, methods=["GET"])
    def new_iocs_length(self, request):
        stats, created = Stats.objects.get_or_create(pk=1)
        new_iocs = {
            "length": stats.new_iocs_count
        }
        return Response(new_iocs)

    @action(detail=False, methods=["GET"])
    def frequent_iocs_length(self, request):
        stats, created = Stats.objects.get_or_create(pk=1)
        frequent_iocs = {
            "length": stats.frequent_iocs_count
        }
        return Response(frequent_iocs)