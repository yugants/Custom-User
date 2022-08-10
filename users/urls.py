from django.urls import path
from users import views

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('ticket/', views.TiketView.as_view(), name='tiket'),
    path('get_token/', views.GetTokenView.as_view(), name='get_token'),
    path('token_filter/', views.TiketFilterView.as_view(), name='all_ticket'),
]
