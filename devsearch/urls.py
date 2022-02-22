from django.urls import path

from . import views

handler404 = 'devsearch.views.not_found'

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('result/<str:query>/', views.result, name='result'),
    path('detail/<str:username>/', views.detail, name='detail'),
]
