from django.urls import path
from . import views
urlpatterns = [
    path('driverLogin', views.driverLogin, name='driverLogin'),
    path('driverRegister', views.driverRegister, name='driverRegister'),
    path('driverHome', views.driverHome, name='driverHome'),
    path('driverProfile', views.driverProfile, name='driverProfile'),
    path('driverBookings', views.driverBookings, name='driverBookings'),
    path('edit_driver_profile', views.edit_driver_profile, name='edit_driver_profile'),
    
]
