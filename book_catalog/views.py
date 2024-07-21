from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Author, Book, Genre, Language, BookSaga, UserBookRelation
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import ChangeBookStatusForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        user_book_relation = UserBookRelation.objects.filter(book=book, user=self.request.user).first()
        context['user_book_relation'] = user_book_relation
        return context

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
    # paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    # template_name ='templates/book_catalog/userbookrelation_list.html'

class AuthorCreateView(PermissionRequiredMixin,CreateView):
    model = Author
    fields = '__all__'
    permission_required = 'book_catalog.add_author'

class AuthorUpdateView(PermissionRequiredMixin,UpdateView):
    model = Author
    fields = '__all__'
    permission_required = 'book_catalog.change_author'

class AuthorDeleteView(PermissionRequiredMixin,DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'book_catalog.delete_author'

class BookCreateView(PermissionRequiredMixin,CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'book_catalog.add_book'

class BookUpdateView(PermissionRequiredMixin,UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'book_catalog.change_book'

class BookDeleteView(PermissionRequiredMixin,DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'book_catalog.delete_book'

def change_book_status(request, pk):
    """
    View function for changing book status.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = ChangeBookStatusForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            UserBookRelation.objects.update_or_create(user = request.user, book = book, defaults = {'status': status})
            return HttpResponseRedirect(reverse('book-detail', args=[str(pk)]))
    else:
        form = ChangeBookStatusForm(initial = {'status': "t"})
    return render(request, 'book_catalog/change_book_status.html', {'form': form, 'book': book})

def delete_book_status(request, pk):
    """
    View function for changing book status.
    """
    book = get_object_or_404(Book, pk=pk)
    UserBookRelation.objects.filter(user = request.user, book = book).delete()
    return HttpResponseRedirect(reverse('book-detail', args=[str(pk)]))



# def add_book(request):
#     if request.method == 'POST':
#         form = BookForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('some-view-name')
#     else:
#         form = BookForm()
#     return render(request, 'add_book.html', {'form': form})