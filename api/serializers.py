from rest_framework import serializers
from todo.models import *


class TodoSerializer(serializers.ModelSerializer):
    """
    A serializer to return the data in a JSON format
    The created and datecompleted fields are read only
    """
    created = serializers.ReadOnlyField()
    datecompleted = serializers.ReadOnlyField()

    class Meta:
        model = Todo
        fields = ['id', 'title', 'memo', 'created', 'datecompleted', 'important']


class TodoCompletedSerializer(serializers.ModelSerializer):
    """
    A serializer to return the data in a JSON format for an item that the user marks as completed
    All fields are read only
    """
    class Meta:
        model = Todo
        fields = ['id']
        read_only_fields = ['title', 'memo', 'created', 'datecompleted', 'important']
