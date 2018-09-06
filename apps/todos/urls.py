# apps/todos/urls.py
from django.urls import path

from . import views

app_name="todos"

urlpatterns = [
    path('', \
            views.ListTodo.as_view(), \
            name="list"),

    path('<int:pk>/', \
            views.DetailTodo.as_view(), \
            name="detail"),
]
