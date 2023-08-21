from django.urls import path
from agent import views


urlpatterns = [
    path('assign-report/<int:agent_id>/', views.assign_report, name='assign_report'),
]
