from django.urls import path
from .views import (
    IocViewSet,
    SourceIocViewSet,
    DateIocViewSet,
    IocTypeViewSet,
    StatsViewSet
)

urlpatterns = [
    path("ioc_feeds", IocViewSet.as_view({
        "get": "list"
    })),
    path('ioc_feeds/sources/<str:source>/', SourceIocViewSet.as_view({
        "get": "get"
    })),
    path('ioc_feeds/sources/<str:source>/length/', SourceIocViewSet.as_view({
        "get": "length"
    })),
    path('ioc_feeds/date', DateIocViewSet.as_view({
        "get": "get"
    })),
    path('ioc_feeds/ioc_type/<str:ioc_type>/', IocTypeViewSet.as_view({
        "get": "get"
    })),
    path('ioc_feeds/ioc_type/<str:ioc_type>/length/', IocTypeViewSet.as_view({
        "get": "length"
    })),
    path('ioc_feeds/stats/new_iocs/length/', StatsViewSet.as_view({
        "get": "new_iocs_length"
    })),
    path('ioc_feeds/stats/frequent_iocs/length/', StatsViewSet.as_view({
        "get": "frequent_iocs_length"
    })),
]