from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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
    # recent_books = Book.objects.all().order_by('-date_finished')[:5]
    recent_books = Book.objects.all().order_by('-id')[:5]
    total_books = Book.objects.all().count()
    # books_this_year = Book.objects.filter(date_finished__year=datetime.now().year).count()
    total_authors=Author.objects.count()
    context = {
        'recent_books': recent_books,
        'total_books': total_books,
        'total_authors': total_authors,
        # 'books_this_year': books_this_year,
        # 'average_books_per_month': average_books_per_month,
    }
    if request.user.is_authenticated:
        books_read_id = UserBookRelation.objects.filter(user=request.user, status='r').order_by('-id')[:3]
        books_read = [Book.objects.get(pk=book.book_id) for book in books_read_id]
        # books_read = Book.objects.filter(pk__in=books_read)
        # average_books_per_month = books_read.count() / (datetime.now().month - books_read.aggregate(Min('date_finished'))['date_finished__min'].month + 1)
        context['books_read'] = books_read

    return render(
        request,
        'index_book.html',
        context = context,
    )


class BookListView(generic.ListView):
    model = Book
    template_name = 'book_list.html'

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

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        books = author.book_set.all().order_by('saga', 'saga_volume')
        context['books'] = books
        return context

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

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        books = author.book_set.all().order_by('saga', 'saga_volume')
        context['books'] = books
        return context

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

# @login_required
# def change_book_status(request, pk):
#     """
#     View function for changing book status.
#     """
#     book = get_object_or_404(Book, pk=pk)
#     if request.method == 'POST':
#         form = ChangeBookStatusForm(request.POST)
#         if form.is_valid():
#             status = form.cleaned_data['status']
#             UserBookRelation.objects.update_or_create(user = request.user, book = book, defaults = {'status': status})
#             return HttpResponseRedirect(reverse('book-detail', args=[str(pk)]))
#     else:
#         status = UserBookRelation.objects.filter(user = request.user, book = book).first()
#         initial_status = status.status if status else 't'
#         form = ChangeBookStatusForm(initial = {'status': initial_status})
#     return render(request, 'book_catalog/change_book_status_form.html', {'form': form, 'book': book})

@login_required
def change_book_status(request, pk, status: str):
    """
    View function for changing book status.
    """
    book = get_object_or_404(Book, pk=pk)
    relation = UserBookRelation.objects.filter(user = request.user, book = book).first()
    if relation:
        if status == 'd':
            relation.delete()
        else:
            relation.status = status
            relation.save()
    elif not relation and status != 'd':
        UserBookRelation.objects.create(user = request.user, book = book, status = status)
    return HttpResponseRedirect(reverse('book-detail', args=[str(pk)]))

# @login_required
# def change_book_status_to_read(request, pk):
#     """
#     View function for changing book status.
#     """
#     book = get_object_or_404(Book, pk=pk)
#     status = UserBookRelation.objects.filter(user = request.user, book = book).first()
#     if status:
#         status.status = 'r'
#         status.save()
#     else:
#         UserBookRelation.objects.create(user = request.user, book = book, status = 'r')
#     return HttpResponseRedirect(reverse('book-detail', args=[str(pk)]))

    # if request.method == 'POST':
    #     form = ChangeBookStatusForm(request.POST)
    #     if form.is_valid():
    #         status = form.cleaned_data['status']
    #         UserBookRelation.objects.update_or_create(user = request.user, book = book, defaults = {'status': status})
    #         return HttpResponseRedirect(reverse('book-detail', args=[str(pk)]))
    # else:
    #     status = UserBookRelation.objects.filter(user = request.user, book = book).first()
    #     initial_status = status.status if status else 't'
    #     form = ChangeBookStatusForm(initial = {'status': initial_status})
    # return render(request, 'book_catalog/change_book_status_form.html', {'form': form, 'book': book})


@login_required
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