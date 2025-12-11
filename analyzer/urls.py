from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('scan/', views.scan, name='scan'),
    path('result/<int:scan_id>/', views.result, name='result'),
    path('history/', views.history, name='history'),
    path('my-scans/', views.my_scans, name='my_scans'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]


