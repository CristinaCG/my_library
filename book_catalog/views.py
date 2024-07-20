from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Author, Book, Genre, Language, BookSaga, UserBookRelation
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    """
    View function for home page of site.
    """
    num_books=Book.objects.all().count()
    num_authors=Author.objects.count()
    return render(
        request,
        'index_book.html',
        context = {'num_books':num_books, 'num_authors':num_authors},
    )


class BookListView(generic.ListView):
    model = Book

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Author

class BookSagaDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = BookSaga

class UerBookRelationListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books of the current user.
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = UserBookRelation
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    # template_name ='templates/book_catalog/userbookrelation_list.html'

