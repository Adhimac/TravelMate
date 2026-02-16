from django.urls import path
from . import views         
urlpatterns = [
    path('rentalPartnerLogin',views.rentalPartnerLogin,name='rentalPartnerLogin'),
    path('rentalPartnerRegister',views.rentalPartnerRegister,name='rentalPartnerRegister'),
    path('rentalPartnerHome',views.rentalPartnerHome,name='rentalPartnerHome'),
    path('addingCars',views.addingCars,name='addingCars'),
    path('rentalPartnerProfile',views.rentalPartnerProfile,name='rentalPartnerProfile'),
    path('rentalPartnerBookings',views.rentalPartnerBookings,name='rentalPartnerBookings'),    
    path('myCars',views.myCars,name='myCars'),
    path('editCar/<int:car_id>/', views.editCar, name='editCar'),
    path('deleteCar/<int:id>/', views.deleteCar, name='deleteCar'),
]