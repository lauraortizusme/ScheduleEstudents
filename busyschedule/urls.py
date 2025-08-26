from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_home, name='home'),  
    path('schedule/', views.schedule_home, name='schedule_home'),
    path('routine/', views.routine_view, name='routine'),  
    path('edit/<int:pk>/modal/', views.edit_schedule_modal, name='edit_schedule_modal'),
    path('delete/<int:pk>/', views.delete_schedule, name='delete_schedule'),
    path('delete-block/<int:pk>/', views.delete_block, name='delete_block'),
]