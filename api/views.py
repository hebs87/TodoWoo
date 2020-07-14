from rest_framework import generics, permissions
from todo.models import *
from .serializers import *


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
