from django.urls import path
from .views import IocViewSet

urlpatterns = [
    path("ioc_feeds", IocViewSet.as_view({
        "get": "list"
    }))
]
