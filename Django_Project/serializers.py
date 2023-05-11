from rest_framework import serializers
from .models import datas

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model= datas
        fields=('query','response')