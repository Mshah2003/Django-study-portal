from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('notes',views.notes,name='notes'),
    path('delete_note/<int:pk>',views.delete_note,name='delete-note'),
    path('notes_detail/<int:pk>',views.NotesDetailView,name='notes-detail'),
    path('homework',views.homework,name='homework'),
    path('update_hw/<int:pk>',views.update_hw,name='update-hw'),
    path('delete_hw/<int:pk>',views.delete_hw,name='delete-hw'),
    path('youtube',views.youtube,name='youtube'),
    path('todo',views.todo,name='todo'),
    path('delete_todo/<int:pk>',views.delete_todo,name='delete-todo'),
    path('update_todo/<int:pk>',views.update_todo,name='update-todo'),
    path('books',views.books,name='books'),
    path('dictionary',views.dictionary,name='dictionary'),
    path('wiki',views.wikipedia,name='wiki'),
]