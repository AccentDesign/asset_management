from django.urls import path

from assets import views


app_name = 'assets'

urlpatterns = [
    path('assets/', views.AssetList.as_view(), name='asset-list'),
    path('assets/create/', views.AssetCreate.as_view(), name='asset-create'),
    path('assets/<int:pk>/update/', views.AssetUpdate.as_view(), name='asset-update'),
    path('assets/<int:pk>/delete/', views.AssetDelete.as_view(), name='asset-delete'),
    path('contacts', views.ContactList.as_view(), name='contact-list'),
    path('contacts/create/', views.ContactCreate.as_view(), name='contact-create'),
    path('contacts/<int:pk>/update/', views.ContactUpdate.as_view(), name='contact-update'),
    path('contacts/<int:pk>/delete/', views.ContactDelete.as_view(), name='contact-delete')
]
