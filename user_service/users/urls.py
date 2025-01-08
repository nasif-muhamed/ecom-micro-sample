from django.urls import path, include
from .views import RegisterView, UserView, UsersView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', UsersView.as_view(), name='users-details'),
    path('register/', RegisterView.as_view(), name='register'),
    path('<int:pk>/', UserView.as_view(), name='user-details'),
    path('token/', TokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('auth/', include("rest_framework.urls")),

]
