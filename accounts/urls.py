from django.urls import path
from .views import UserRegistrationForm_View, UserLoginForm_View, UserLogoutForm_View, UserProfileUpdateForm_View

urlpatterns = [
    path('register/', UserRegistrationForm_View.as_view(), name='register'),
    path('login/', UserLoginForm_View.as_view(), name='login'),
    path('logout/', UserLogoutForm_View.as_view(), name='logout'),
    path('update_profile/', UserProfileUpdateForm_View.as_view(), name='update_profile'),
]
