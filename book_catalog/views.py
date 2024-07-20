from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Author, Book, Genre, Language, BookSaga, UserBookRelation
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ChangeBookStatusForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

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

# @permision_required('book_catalog.can_mark_returned')
# class ChangeBookStatusView(LoginRequiredMixin, generic.UpdateView):
#     template_name = 'book_catalog/change_book_status.html'
#     model = UserBookRelation
#     fields = ['status']  # Asumiendo que quieres actualizar el campo 'status'
#     success_url = '/book/'  # Asegúrate de cambiar esto a una URL adecuada

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Asumiendo que tienes acceso al libro y al usuario en esta vista
#         book_id = self.kwargs.get('book_id')
#         user = self.request.user
#         user_book_relation = UserBookRelation.objects.filter(book_id=book_id, user=user).first()
#         context['user_book_relation'] = user_book_relation
#         return context

#     def get_queryset(self):
#         return super().get_queryset().filter(user=self.request.user)

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