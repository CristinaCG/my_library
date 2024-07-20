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
    path('book/<int:pk>/change-status/', views.change_book_status, name='change-book-status'),
    # path('book/<int:book_id>/change-status/', views.ChangeBookStatusView.as_view(), name='change-book-status'),
    path('book/<int:pk>/delete-status/', views.delete_book_status, name='delete-book-status'),
]
