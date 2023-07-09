
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostCollectionView.as_view(), name='posts'),
    path('<int:pk>/', views.PostSingletonView.as_view())
]
