from django.shortcuts import render
from .models import Book, Author
from django.views import generic

def index(request):
    num_books=Book.objects.all().count()
    num_authors=Author.objects.count()
    return render(
        request,
        'index_book.html',
        context = {'num_books':num_books, 'num_authors':num_authors},
    )


class BookListView(generic.ListView):
    model = Book

class BookDetailView(generic.DetailView):
    model = Book
