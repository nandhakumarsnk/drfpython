from rest_framework import serializers
from .models import *

class subscriptionserializer(serializers.ModelSerializer):
    class Meta:
        model=Subscription
        fields="__all__"

class categoryserializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"

class items_serializer(serializers.ModelSerializer):
    class Meta:
        model=Items
        fields="__all__"