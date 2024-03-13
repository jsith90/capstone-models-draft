from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('table_booking', views.table_booking, name='table_booking'),
    path('table_booking_submit', views.table_booking_submit, name='table_booking_submit'),
    path('user-panel', views.user_panel, name='user_panel'),
    path('user-update/<int:id>', views.user_update, name='user_update'),
    path('user-update-submit/<int:id>', views.user_update_submit, name='user_update_submit'),
    path('staff-panel', views.staff_panel, name='staff_panel'),
    path('delete_booking/<booking_id>', views.delete_booking, name='delete_booking'),
]
