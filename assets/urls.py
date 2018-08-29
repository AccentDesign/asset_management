from django.urls import path

from assets import views


app_name = 'assets'

urlpatterns = [
    path('assets/', views.AssetRootList.as_view(), name='asset-list'),
    path('assets/create/', views.AssetCreate.as_view(), name='asset-create'),
    path('assets/<uuid:pk>/nodes/', views.AssetNodeList.as_view(), name='asset-list-nodes'),
    path('assets/<uuid:pk>/update/', views.AssetUpdate.as_view(), name='asset-update'),
    path('assets/<uuid:pk>/delete/', views.AssetDelete.as_view(), name='asset-delete'),
    path('assets/<uuid:pk>/copy/', views.AssetCopy.as_view(), name='asset-copy'),
    path('asset-types/', views.AssetTypeList.as_view(), name='asset-type-list'),
    path('asset-types/create/', views.AssetTypeCreate.as_view(), name='asset-type-create'),
    path('asset-types/<uuid:pk>/update/', views.AssetTypeUpdate.as_view(), name='asset-type-update'),
    path('asset-types/<uuid:pk>/delete/', views.AssetTypeDelete.as_view(), name='asset-type-delete'),
    path('contacts/', views.ContactList.as_view(), name='contact-list'),
    path('contacts/create/', views.ContactCreate.as_view(), name='contact-create'),
    path('contacts/<uuid:pk>/update/', views.ContactUpdate.as_view(), name='contact-update'),
    path('contacts/<uuid:pk>/delete/', views.ContactDelete.as_view(), name='contact-delete'),
    path('files/', views.FileList.as_view(), name='file-list'),
    path('files/upload/', views.FileUpload.as_view(), name='file-upload'),
    path('notes/', views.NoteList.as_view(), name='note-list'),
    path('notes/create/', views.NoteCreate.as_view(), name='note-create'),
    path('notes/<uuid:pk>/update/', views.NoteUpdate.as_view(), name='note-update'),
    path('notes/<uuid:pk>/delete/', views.NoteDelete.as_view(), name='note-delete'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('tasks/', views.TaskList.as_view(), name='task-list'),
    path('tasks/<uuid:pk>/update/', views.TaskUpdate.as_view(), name='task-update'),
    path('task-priorities/', views.TaskPriorityList.as_view(), name='task-priority-list'),
    path('task-priorities/create/', views.TaskPriorityCreate.as_view(), name='task-priority-create'),
    path('task-priorities/<uuid:pk>/update/', views.TaskPriorityUpdate.as_view(), name='task-priority-update'),
    path('task-priorities/<uuid:pk>/delete/', views.TaskPriorityDelete.as_view(), name='task-priority-delete'),
    path('task-types/', views.TaskTypeList.as_view(), name='task-type-list'),
    path('task-types/create/', views.TaskTypeCreate.as_view(), name='task-type-create'),
    path('task-types/<uuid:pk>/update/', views.TaskTypeUpdate.as_view(), name='task-type-update'),
    path('task-types/<uuid:pk>/delete/', views.TaskTypeDelete.as_view(), name='task-type-delete'),
]
