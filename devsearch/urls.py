from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('result/<str:keyword>/', views.result, name='result'),
    path('detail/<str:username>/', views.detail, name='detail'),
]
