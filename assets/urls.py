from django.urls import path

from assets import views


app_name = 'assets'

urlpatterns = [
    path('', views.AssetList.as_view(), name='asset-list'),
    path('create/', views.AssetCreate.as_view(), name='asset-create'),
    path('<int:pk>/update/', views.AssetUpdate.as_view(), name='asset-update'),
    path('<int:pk>/delete/', views.AssetDelete.as_view(), name='asset-delete')
]
