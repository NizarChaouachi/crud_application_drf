from django.urls import path
from .views import Notes, NotesDetail

urlpatterns=[
    path('',Notes.as_view()),
    path('<str:pk>/',NotesDetail.as_view())
]