from django.urls import path
from . import views

urlpatterns = [
    path('send', views.send_money, name='send_money'),
    path('request', views.request_money, name='request_money'),
    path('notifications', views.notifications, name='notifications'),
    path('transactions', views.transaction_history, name='transactions'),
    path('notifications/accept/<int:transaction_id>/', views.accept_transaction, name='accept_transaction'),
    path('notifications/reject/<int:transaction_id>/', views.reject_transaction, name='reject_transaction'),
]
