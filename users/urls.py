from django.urls import path
from . import views
app_name = "users"
urlpatterns=[
    path('register/',views.register,name='register'),
    path('profile/',views.profile_pg,name='profile'),
    path('login/',views.custom_login,name='login'),
    path('logout/',views.custom_logout,name='logout'),
    path('edit-profile/',views.edit_profile,name='edit'),
    path('request_order/<str:med_name>/<str:pharma_email>/<str:pharma_name>/',views.request_order,name='request_order'),
    path('activate/<uidb64>/<token>',views.activate, name='activate'),
    ]