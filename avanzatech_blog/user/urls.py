from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('success/', views.success_page, name='success_page'),
    path('login-page', views.login_page, name='login_page')
]

