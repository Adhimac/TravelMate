from django.urls import path
from . import views
urlpatterns = [
    path('driverLogin',views.driverLogin,name='driverLogin'),
    path('driverRegister',views.driverRegister,name='driverRegister'),
    path('driverHome',views.driverHome,name='driverHome'),
    path('driverProfile',views.driverProfile,name='driverProfile'),
]
