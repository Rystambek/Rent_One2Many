from django.contrib import admin
from django.urls import path

from app.views.car import CarView,CarIDView,all,CarallView
from app.views.company import CompanyView


urlpatterns = [
    path('company/<int:id>/car/',CarView.as_view()),
    path('car/',CarallView.as_view()),
    path('company/<int:id>',CompanyView.as_view()),
    path("company/",CompanyView.as_view()),
    path("company/<int:car_id>/car/<int:id>",CarIDView.as_view()),
    path('',all)
]