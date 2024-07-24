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
    path('book/<int:pk>/change-status/<str:status>/', views.change_book_status, name='change-book-status'),
    # path('book/<int:pk>/delete-status/', views.delete_book_status, name='delete-book-status'),
    path('author/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),
    path('book/create/', views.BookCreateView.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
]
