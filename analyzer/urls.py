from django.urls import path
from .views import AnalyzeArtifactView, TaskListView, TaskActionView, TaskDetailView

urlpatterns = [
    path('analyze/', AnalyzeArtifactView.as_view(), name='analyze_artifact'),
    path('tasks/', TaskListView.as_view(), name='list_tasks'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:pk>/<str:action>/', TaskActionView.as_view(), name='task_action'),
]
