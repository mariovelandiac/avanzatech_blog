from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListCreatePostView.as_view(), name="post-list-create"),
    path('<int:pk>/', views.RetrieveUpdateDeletePostView.as_view(), name="post-retrieve-update-delete"),
]

