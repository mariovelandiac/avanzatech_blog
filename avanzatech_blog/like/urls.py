from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListCreateLikeView.as_view(), name="like-list-create"),
    path('<int:user>/<int:post>', views.DeleteLikeViewLikeView.as_view(), name="like-delete"),
]

