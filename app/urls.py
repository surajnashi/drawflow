from django.urls import path
from . import views

urlpatterns = [
    path('home',views.home),
    path('createUser',views.createUser),
    path('verify/',views.verifyUser),
    path("success/",views.success),
    path('logout',views.logout_form),
    
]
