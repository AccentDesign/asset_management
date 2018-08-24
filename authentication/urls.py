from django.contrib.auth.views import PasswordResetView
from django.urls import path, include

from authentication import views


urlpatterns = [
    path('password_reset/',
         PasswordResetView.as_view(html_email_template_name='emails/password_reset_email.html'),
         name='password_reset'),
    path('my-profile/', views.ProfileUpdate.as_view(), name='my_profile'),
    path('teams/create/', views.TeamCreate.as_view(), name='team-create'),
    path('teams/<uuid:pk>/activate/', views.TeamActivate.as_view(), name='team-activate'),
    path('', include('django.contrib.auth.urls')),
]
