from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.MainView.as_view()),
    path('reset/', views.ResetView.as_view()),
    path('retrieve/<get_type>/<int:active>/', views.RetrieveView.as_view()),
    path('detail-retrieve/<get_type>/', views.RetrieveDetailView.as_view()),
    path('create/<create_type>/', views.CreateView.as_view()),
    path('update/<update_type>/',views.UpdateView.as_view()),
    path('delete/<delete_type>/', views.DeleteView.as_view()),
    path('join/<join_type>/', views.JoinView.as_view()),
]
