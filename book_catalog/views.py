from django.shortcuts import render
from .models import Author, Book, Genre, Language, BookSaga
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