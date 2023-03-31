from rest_framework import serializers
from .models import Ioc

# basically converts your model into JSON format
# think of it like Java's implements serializable where converts a POJO to readable JSON
class IoCSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ioc
        fields = "__all__"  