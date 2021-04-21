from django.urls import path
from . import views

app_name='todo'

urlpatterns = [
    path('', views.index, name='index'),
    path('join/', views.join, name='join'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('cal/', views.cal, name='cal'),
    path('addTodo/', views.addTodo, name='addTodo'),
    path('delTodo/', views.delTodo, name='delTodo'),
    path('getTodo/', views.getTodo, name='getTodo'),
]
