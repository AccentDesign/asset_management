from django.contrib.auth.views import PasswordResetView
from django.urls import path, include

from app import routers
from authentication import api, views

router = routers.DefaultRouter()

router.register(r'users', api.UserViewSet)

urlpatterns = [
    path('password_reset/',
         PasswordResetView.as_view(html_email_template_name='emails/password_reset_email.html'),
         name='password_reset'),
    path('my-profile/', views.ProfileUpdate.as_view(), name='my_profile'),
    path('teams/create/', views.TeamCreate.as_view(), name='team-create'),
    path('', include('django.contrib.auth.urls')),
]
