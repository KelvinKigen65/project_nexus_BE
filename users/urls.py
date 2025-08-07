from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, CreateUserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='auth_login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/create/', CreateUserProfileView.as_view(), name='create-profile'),
]
