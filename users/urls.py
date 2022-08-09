from django.urls import path
from users import views

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('ticket/', views.TiketView.as_view(), name='tiket'),
]
