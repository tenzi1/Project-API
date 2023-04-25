from django.urls import path
from .views import  ProjectView, upload_project,ProjectSummary, CountProjectBudget


urlpatterns = [
    path("", ProjectView.as_view()),
    path('upload/projects/', upload_project , name='upload-projects'),
    path('projects/budget/count/',CountProjectBudget.as_view()),
    path("projects/summary/", ProjectSummary.as_view()),
   
]