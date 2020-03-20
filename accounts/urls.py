from django.urls import path
from . import views
urlpatterns = [

    path('register_page/', views.registerpage, name = 'register_page'),
    path('login/', views.loginpage, name = 'login'),
    path('logout/', views.logoutuser, name = 'logout'),
    path('', views.home, name = 'home'),
    path('products/', views.products, name = 'products'),
    path('customer/<str:pk>/', views.customer, name = 'customer'),
    path('create_order/<str:pk>', views.createorder, name = 'create_order'),
    path('update_order/<str:pk>', views.updateorder, name = 'update_order'),
    path('delete_order/<str:pk>', views.deleteorder, name = 'delete_order'),
    

]
