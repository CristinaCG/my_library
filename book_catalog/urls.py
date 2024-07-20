from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'), 
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('saga/<int:pk>', views.BookSagaDetailView.as_view(), name='saga-detail'),
    path('mybooks/', views.UerBookRelationListView.as_view(), name='my-books'),
]
