from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('list', views.list_all, name='list'),
    path('view', views.view_all, name='view'),
    path('average', views.view_average, name='average'),
    path('rate', views.rate, name='rate'),
]