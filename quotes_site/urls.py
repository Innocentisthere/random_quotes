"""
URL configuration for quotes_site project.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("quotes/", include("quotes_app.urls")),
    path('admin/', admin.site.urls),
]
