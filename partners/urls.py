from django.urls import path

from . import views

app_name = 'partners'

urlpatterns = [
    path('upload-create-policy/', views.upload_create_policy, name='upload-create-policy'),
]