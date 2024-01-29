from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListCreateUpdateLikeView.as_view(), name="like-list-create-update"),
]

