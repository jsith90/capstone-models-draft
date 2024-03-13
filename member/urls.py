from django.urls import path
from . import views

urlpatterns = [
    path('login_user', views.login_user, name="login_user"),
    path('logout_user', views.logout_user, name="logout"),
    path('register_user', views.register_user, name="register_user"),
    path('member/details_update/<int:id>/', views.details_update, name='details_update'),
    path('password-update/', views.password_update, name='password_update'),
]