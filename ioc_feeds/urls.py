from django.urls import path
from .views import (
    IocViewSet,
    SourceIocViewSet,
    DateIocViewSet,
    IocTypeViewSet
)

urlpatterns = [
    path("ioc_feeds", IocViewSet.as_view({
        "get": "list"
    })),
    path('ioc_feeds/sources/<str:source>/', SourceIocViewSet.as_view({
        "get": "get"
    })),
    path('ioc_feeds/date', DateIocViewSet.as_view({
        "get": "get"
    })),
    path('ioc_feeds/ioc_type/<str:ioc_type>/', IocTypeViewSet.as_view({
        "get": "get"
    })),
]