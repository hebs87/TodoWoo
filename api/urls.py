from django.urls import path, include
from .views import *

urlpatterns = [
    path('todos/completed/', TodoCompleteList.as_view(), name='completed_todos'),
]
