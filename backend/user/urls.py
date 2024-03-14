from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('sign-up/', views.UserCreateView.as_view(), name='sign-up'),
    path('login-page', views.login_page, name='login_page')
]

