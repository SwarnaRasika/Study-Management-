from django.contrib import admin
from django.urls import path, include
from studies import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.home, name='home'),  # Home page
    path('', include('studies.urls')),  # Study app URL inclusion
]
