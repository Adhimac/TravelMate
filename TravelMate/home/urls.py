from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('userLogin',views.userLogin,name='userLogin'),
    path('userReg',views.userReg,name='userReg'),
    path('userHome',views.userHome,name='userHome'),
    path('about',views.about,name='about'),
    path('destination',views.destination,name='destination'),
    path('coTraveler',views.coTraveler,name='coTraveler'),
   
]
