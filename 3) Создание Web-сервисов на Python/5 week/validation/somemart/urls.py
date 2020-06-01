# from django.urls import include, path
from django.conf.urls import url

from .views import AddItemView, GetItemView, PostReviewView

urlpatterns = [
    url('api/v1/goods/', AddItemView.as_view()),
    url('api/v1/goods/<int:item_id>/', GetItemView.as_view()),
    url('api/v1/goods/<int:item_id>/reviews/', PostReviewView.as_view()),
]
