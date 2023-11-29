from django.contrib import admin
from django.urls import path

from app.views.car import CarView
from app.views.rent_car import RentView,all


urlpatterns = [
    path('car/<int:id>',CarView.as_view()),
    path('car/',CarView.as_view()),
    path('rent/',RentView.as_view()),
    path('rent/<int:id>',RentView.as_view()),
    path('',all)
]