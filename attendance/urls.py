from django.urls import path
from . import views

urlpatterns = [
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path('submit/', views.submit_attendance, name='submit_attendance'),
]
