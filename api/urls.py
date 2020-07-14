from django.urls import path, include
from .views import *

urlpatterns = [
    # Todos
    path('todos', TodoListCreate.as_view(), name='todos'),
    path('todos/<int:pk>', TodoRetrieveUpdateDestroy.as_view(), name='single_todo'),
    path('todos/<int:pk>/completed', TodoComplete.as_view(), name='todo_completed'),
    path('todos/completed', TodoCompleteList.as_view(), name='completed_todos_list'),

    # Auth
    path('signup', signup, name='signup'),
    path('login', login, name='login'),
]
