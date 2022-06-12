from django.urls import path
from . import views


boosts_list = views.BoostViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

boosts_details = views.BoostViewSet.as_view({
    'put': 'partial_update',
})

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('boosts/', boosts_list, name='boosts'),
    path('boosts/<int:pk>/', boosts_details, name='boosts'),
    path('update_coins/', views.update_coins, name='update_coins'),
    path('core/', views.get_core, name='core'),
]