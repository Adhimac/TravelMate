from django.urls import path
from . import views
urlpatterns = [
       path('adminLogin', views.adminLogin, name='adminLogin'),
       path('adminHome', views.adminHome, name='adminHome'),
       path('adminUserManagement', views.adminUserManagement, name='adminUserManagement'),
       path('adminDriverManagement', views.adminDriverManagement, name='adminDriverManagement'),
       path('adminCarManagement', views.adminCarManagement, name='adminCarManagement'),
       path('viewBookings', views.viewBookings, name='viewBookings'),
       path('drivers/', views.driverRequests, name='driverRequests'),
       path('approve/<int:driver_id>/', views.approveDriver, name='approveDriver'),
       path('reject/<int:driver_id>/', views.rejectDriver, name='rejectDriver'),
       path('rentalPartnerRequests/', views.rentalPartnerRequests, name='rentalPartnerRequests'),
       path('partners/', views.rentalPartnerManagement, name='rentalPartnerManagement'),
    path(
        'approveRentalPartners/',
        views.approveRentalPartners,
        name='approveRentalPartners'
    ),
    path(
        'approvePartner/<int:id>/',
        views.approvePartner,
        name='approvePartner'
    ),
    path(
    'rejectPartner/<int:id>/',
    views.rejectPartner,
    name='rejectPartner'
),
    path('adminPartnerManagement', views.adminPartnerManagement, name='adminPartnerManagement'),


]                