from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("random", views.r, name="r"),
    path("wiki/edit/<str:title>", views.edit, name="edit")
]
