from django.contrib import admin
from django.urls import path, include
from api.views import home

urlpatterns = [
    path("", home, name="home"),  # para renderizar home.html
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),  # para incluir las rutas de la app api
]
