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
    path('hireNow',views.hireNow,name='hireNow'),
    path('rentCar',views.rentCar,name='rentCar'),
    path('rentNow',views.rentNow,name='rentNow'),
    path('destination',views.destination,name='destination'),
]
