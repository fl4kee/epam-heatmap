from django.urls import path

from . import views

urlpatterns = [
    path("spb/", views.show_heatmap, name="heatmap_spb"),
    path("ekb/", views.show_heatmap, name="heatmap_ekb"),
    path("msk/", views.show_heatmap, name="heatmap_msk"),
    path("", views.show_default),
]
