from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('adding_page/', views.adding_page, name='adding_page'),
    path('<int:news_id>/', views.detail, name='detail'),
]
