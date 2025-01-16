
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home',),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_user, name='register'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:boo>', views.category, name='category'),
]
