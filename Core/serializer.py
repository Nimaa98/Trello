from rest_framework import serializers
from .models import Image


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ("id","Image","alt_text","create_at")
        