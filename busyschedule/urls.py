from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_schedule, name='schedule'),
    path('edit/<int:pk>/', views.edit_schedule, name='edit_schedule'),    # NUEVO
    path('delete/<int:pk>/', views.delete_schedule, name='delete_schedule'),  # NUEVO
]
