from django.urls import path, include
from .views import *

urlpatterns = [
    path('todos', TodoListCreate.as_view(), name='todos'),
    path('todos/completed', TodoCompleteList.as_view(), name='completed_todos'),
]
