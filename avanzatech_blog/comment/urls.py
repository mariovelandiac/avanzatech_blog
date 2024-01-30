from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListCreateCommentView.as_view(), name="comment-list-create"),
    path('<int:pk>/', views.DeleteCommentView.as_view(), name="comment-delete"),
]
