from django.urls import path, include
from .admin_site import admin_site

app_name = 'adminpanel'

urlpatterns = [
    path('', admin_site.urls),
]
