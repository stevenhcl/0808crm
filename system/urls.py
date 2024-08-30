from django.urls import path
from . import views

#设置命名空间名称
app_name = 'system'

urlpatterns = [
    path('login_register/', views.login_register, name='login_register'),
    path('register/', views.register, name='register'),
    path('unique_username/', views.unique_username, name='unique_username'),
    path('unique_email/', views.unique_email, name='unique_email'),
    path('send_email/', views.send_email, name='send_email'),
    path('active_accounts/', views.active_accounts, name='active_accounts'),
]
