from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/files/', views.file_crud, name='file_crud'),
    path('api/files/raw/', views.file_raw, name='file_raw'),
    path('api/folders/', views.folder_crud, name='folder_crud'),
    path('api/ai-chat/', views.ai_chat, name='ai_chat'),
    path('api/history/', views.chat_history_api, name='chat_history_api'),
    path('clase8/', views.presentacion_clase8, name='presentacion_clase8'),
]



