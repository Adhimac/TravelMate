from django.urls import path
from . import views
urlpatterns = [
       path('adminLogin', views.adminLogin, name='adminLogin'),
       path('adminHome', views.adminHome, name='adminHome'),
       path('adminUserManagement', views.adminUserManagement, name='adminUserManagement'),
       path('adminDriverManagement', views.adminDriverManagement, name='adminDriverManagement'),
       path('adminCarManagement', views.adminCarManagement, name='adminCarManagement'),
       path('viewBookings', views.viewBookings, name='viewBookings'),
]               