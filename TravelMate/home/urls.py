from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('userLogin',views.userLogin,name='userLogin'),
    path('userReg',views.userReg,name='userReg'),
    path('userHome',views.userHome,name='userHome'),
    path('about',views.about,name='about'),
    path('coTraveler',views.coTraveler,name='coTraveler'),
    path('userProfile',views.userProfile,name='userProfile'),
    path('hireDriver',views.hireDriver,name='hireDriver'),
    path('hire-now/<int:driver_id>/', views.hireNow, name='hireNow'),
    path('rentCar',views.rentCar,name='rentCar'),
    path('rentNow/<int:car_id>/',views.rentNow,name='rentNow'),
    path('destination',views.destination,name='destination'),
    path('payment/<int:car_id>/',views.payment,name='payment'),
    path('profileList',views.profileList,name='profileList'),
    path('profileDetail/<int:user_id>/',views.profileDetail,name='profileDetail'),
    path('connect_traveler/<int:user_id>/', views.connect_traveler, name='connect_traveler'),
]
