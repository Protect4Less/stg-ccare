from django.urls import path

from . import views

app_name = 'claim'

urlpatterns = [
    path('pending-amount/', views.pending_payment, name='pending-payment'),
    path('received_payment/', views.received_payment, name='received-payment'),
    # path('details/<str:id>/', views.details, name='details'),
    # path('code-list/', views.code_list, name='code-list'),
    # path('commission/', views.commission, name='commission'),
    # path('document-sent/', views.document_sent_ajax, name='document_sent'),
    # path('document_file/', views.document_file, name='document_file'),
]