from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/tasks/', views.get_tasks, name='get_tasks'),
    path('api/tasks/create/', views.create_task, name='create_task'),
    path('api/tasks/update/<int:task_id>/', views.update_task, name='update_task'),
    path('api/tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),
]
