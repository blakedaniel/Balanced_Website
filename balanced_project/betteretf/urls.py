from django.urls import path
from . import views

urlpatterns = [
    path('betteretf/', views.HomeView)
]
