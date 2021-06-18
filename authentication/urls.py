from django.contrib.auth.views import PasswordResetView
from django.urls import path, include

from authentication import views


urlpatterns = [
    path('password_reset/',
         PasswordResetView.as_view(html_email_template_name='emails/password_reset_email.html'),
         name='password_reset'),
    path('my-profile/', views.ProfileUpdate.as_view(), name='my_profile'),
    path('collections/create/', views.CollectionCreate.as_view(), name='collection-create'),
    path('collections/<uuid:pk>/activate/', views.CollectionActivate.as_view(), name='collection-activate'),
    path('collections/<uuid:pk>/update/', views.CollectionUpdate.as_view(), name='collection-update'),
    path('collections/<uuid:pk>/delete/', views.CollectionDelete.as_view(), name='collection-delete'),
    path('', include('django.contrib.auth.urls')),
]
