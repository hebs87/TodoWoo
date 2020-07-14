from rest_framework import generics, permissions
from todo.models import *
from .serializers import *
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


# Create your views here.
@csrf_exempt
def signup(request):
    """
    Allow users to signup without the need for a csrf token
    """
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(data['username'], password=data['password'])
            user.save()
            token = Token.objects.create(user=user)
            json_response = {
                'token': str(token),
            }
            return JsonResponse(json_response, status=201)
        except IntegrityError:
            json_response = {
                'error': 'That username has already been taken. Please choose a new username',
            }
            return JsonResponse(json_response, status=400)


@csrf_exempt
def login(request):
    """
    Allow users to login and get the token
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is None:
            json_response = {
                'error': 'Could not login. Please check the username and password.',
            }
            return JsonResponse(json_response, status=400)
        try:
            token = Token.objects.get(user=user)
        except:
            token = Token.objects.create(user=user)

        json_response = {
            'token': str(token),
        }

        return JsonResponse(json_response, status=201)


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
