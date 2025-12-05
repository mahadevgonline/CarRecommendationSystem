from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.index),
    path('register/', views.register),
    path('login/', views.login),
    path('user/', views.user),
    path('adminp/', views.admin),
    path('add-car/', views.add_car),
    path('cars/', views.cars),
    path('view-car/<id>/', views.view_car),
    path('edit-car/<id>/', views.edit_car),
    path('delete-car/<id>/', views.delete_car),
    path('car-detail/<id>/', views.car_detail),
    path('compare/', views.compare),
    path('collections/', views.collections),
    path('add-favorite/<id>/', views.add_favorite),
    path('favorites/', views.favorites),
    path('remove-favorite/<id>/', views.remove_favorite),
    path('profile/', views.profile),
    path('products/', views.products),
    path('add-product/', views.add_product)
]