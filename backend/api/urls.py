from django.urls import path
from . import views

urlpatterns = [
    path('classes/', views.api_classes),
    path('classes/<int:id>/', views.api_classes_delete),
]