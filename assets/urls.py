from django.urls import path

from assets import views


app_name = 'assets'

urlpatterns = [
    path('assets/', views.AssetList.as_view(), name='asset-list'),
    path('assets/create/', views.AssetCreate.as_view(), name='asset-create'),
    path('assets/<int:pk>/update/', views.AssetUpdate.as_view(), name='asset-update'),
    path('assets/<int:pk>/delete/', views.AssetDelete.as_view(), name='asset-delete'),
    path('assets/<int:pk>/copy/', views.AssetCopy.as_view(), name='asset-copy'),
    path('asset-types/', views.AssetTypeList.as_view(), name='asset-type-list'),
    path('asset-types/create/', views.AssetTypeCreate.as_view(), name='asset-type-create'),
    path('asset-types/<int:pk>/update/', views.AssetTypeUpdate.as_view(), name='asset-type-update'),
    path('asset-types/<int:pk>/delete/', views.AssetTypeDelete.as_view(), name='asset-type-delete'),
    path('contacts', views.ContactList.as_view(), name='contact-list'),
    path('contacts/create/', views.ContactCreate.as_view(), name='contact-create'),
    path('contacts/<int:pk>/update/', views.ContactUpdate.as_view(), name='contact-update'),
    path('contacts/<int:pk>/delete/', views.ContactDelete.as_view(), name='contact-delete'),
    path('notes/', views.NoteList.as_view(), name='note-list'),
    path('notes/create/', views.NoteCreate.as_view(), name='note-create'),
    path('notes/<int:pk>/update/', views.NoteUpdate.as_view(), name='note-update'),
    path('notes/<int:pk>/delete/', views.NoteDelete.as_view(), name='note-delete'),
    path('tasks/', views.TaskList.as_view(), name='task-list'),
    path('tasks/<int:pk>/update/', views.TaskUpdate.as_view(), name='task-update'),
    path('task-types/', views.TaskTypeList.as_view(), name='task-type-list'),
    path('task-types/create/', views.TaskTypeCreate.as_view(), name='task-type-create'),
    path('task-types/<int:pk>/update/', views.TaskTypeUpdate.as_view(), name='task-type-update'),
    path('task-types/<int:pk>/delete/', views.TaskTypeDelete.as_view(), name='task-type-delete'),
]
