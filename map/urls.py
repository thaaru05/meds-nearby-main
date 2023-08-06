from django.urls import path
from . import views
app_name = "map"

urlpatterns=[
    path('direction/',views.direction,name='direction'),
]