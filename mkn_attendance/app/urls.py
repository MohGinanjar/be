from app import views
from django.urls import path

urlpatterns = [
    path('auth/register',views.RegisterAPIView.as_view(),name='register'),
    path('auth/login', views.LoginAPIView.as_view(), name="login"),
    path('clock_in', views.clockin, name="clock_in"),
    path('list_project', views.ProjectListView.as_view(), name="list_project"),
    
    path('list_project_user', views.ListProjectUserView.as_view(), name="list_project_user"),
]
