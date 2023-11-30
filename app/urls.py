from django.contrib import admin
from django.urls import path

from app.views.car import CarView


urlpatterns = [
    path('car/<int:id>',CarView.as_view()),
    path('car/',CarView.as_view()),
    path('',all)
]