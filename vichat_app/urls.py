from django.urls import path
from . import views


urlpatterns =[
    path('cats/', views.cats)
]