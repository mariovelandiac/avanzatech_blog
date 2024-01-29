from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListCreateCommentView.as_view(), name="comment-list-create"),
    path('<int:user>/<int:post>/', views.DeleteCommentView.as_view(), name="comment-delete"),
]
