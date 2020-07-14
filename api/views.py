from rest_framework import generics, permissions
from todo.models import *
from .serializers import *
from django.utils import timezone


# Create your views here.
class TodoCompleteList(generics.ListAPIView):
    """
    A view to return a list of completed Todos
    """
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Ensure the logged in user only gets their Todos that have been completed
    def get_queryset(self):
        user = self.request.user
        todos = Todo.objects.filter(user=user, datecompleted__isnull=False).order_by('-datecompleted')
        return todos


class TodoListCreate(generics.ListCreateAPIView):
    """
    A view to allow creating and listing Todos
    """
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Ensure the logged in user only gets their Todos that have been completed
    def get_queryset(self):
        user = self.request.user
        todos = Todo.objects.filter(user=user, datecompleted__isnull=True)
        return todos

    # Set the user field to the user who is creating the item when saving it to the DB
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    A view to allow updating and deleting Todos
    """
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Ensure the logged in user only gets their Todos that have been completed
    def get_queryset(self):
        user = self.request.user
        todos = Todo.objects.filter(user=user)
        return todos


class TodoComplete(generics.UpdateAPIView):
    """
    A view to allow marking Todos as completed
    """
    serializer_class = TodoCompletedSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Ensure the logged in user only gets their Todos that have been completed
    def get_queryset(self):
        user = self.request.user
        todos = Todo.objects.filter(user=user)
        return todos

    # Update the datecompleted field to the current date/time when marking as completed
    def perform_update(self, serializer):
        serializer.instance.datecompleted = timezone.now()
        serializer.save()
