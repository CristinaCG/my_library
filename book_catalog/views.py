from typing import Any
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Author, Book, BookSaga, UserBookRelation, Language, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django import forms

def index(request):
    """
    View function for home page of site.
    """
    # recent_books = Book.objects.all().order_by('-date_finished')[:5]
    recent_books = Book.objects.all().order_by('-publish_date')[:5]
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
        books_read_id = UserBookRelation.objects.filter(user=request.user, status='i').order_by('-id')[:3]
        books_read = [Book.objects.get(pk=book.book_id) for book in books_read_id]
        # books_read = Book.objects.filter(pk__in=books_read)
        # average_books_per_month = books_read.count() / (datetime.now().month - books_read.aggregate(Min('date_finished'))['date_finished__min'].month + 1)
        context['books_read'] = books_read

    return render(
        request,
        'index_book.html',
        context = context,
    )

################# List Views #################

class BookListView(generic.ListView):
    """
    Generic class-based view listing books.
    """
    model = Book
    template_name = 'book_list.html'

    def get_context_data(self, **kwargs):
        """
        Recent book list
        """
        context = super().get_context_data(**kwargs)
        context["recent_books"] = Book.objects.all().order_by('-publish_date')[:5]
        return context

class AuthorListView(generic.ListView):
    """
    Generic class-based view listing authors.
    """
    model = Author

    def get_context_data(self, **kwargs: Any):
        """
        Obtain an author list of authors that has books published recently
        """
        context = super().get_context_data(**kwargs)
        context["recent_books"] = Book.objects.all().order_by('-publish_date')[:5]
        return context

class UserBookRelationListView(LoginRequiredMixin, generic.ListView):
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

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["recent_books"] = Book.objects.all().order_by('-publish_date')[:5]
        return context

################# Detail Views #################

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    """
    Generic class-based view detail of a book.
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        user_book_relation = UserBookRelation.objects.filter(book=book, user=self.request.user).first()
        context['user_book_relation'] = user_book_relation
        return context

class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    """
    Generic class-based view detail of an author.
    """
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
    """
    Generic class-based view detail of a book saga.
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = BookSaga
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        saga = self.get_object()
        relations = [0]*len(saga.book_set.all())
        for i, book in enumerate(saga.book_set.all()):
            relation = UserBookRelation.objects.filter(book=book, user=self.request.user).first()
            if relation: 
                if relation.status == 'r':
                    relations[i] = 3
                if relation.status == 'i':
                    relations[i] = 2
                if relation.status == 't':
                    relations[i] = 1
        if sum(relations) == 3*len(saga.book_set.all()):
            context['user_saga_relation'] = 'r'
        elif sum(relations) >= len(saga.book_set.all())+1+2:
            context['user_saga_relation'] = 'i'
        elif sum(relations) >= len(saga.book_set.all()):
            context['user_saga_relation'] = 't'
        # else:
        #     context['user_saga_relation'] = 'Add to my list'
        return context

################# Create Views #################

class AuthorCreateView(PermissionRequiredMixin,CreateView):
    """
    Generic class-based view for creating an author.
    """
    model = Author
    fields = '__all__'
    permission_required = 'book_catalog.add_author'
    template_name = 'book_catalog/author_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['first_name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        form.fields['last_name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        form.fields['year_of_birth'].widget = forms.TextInput(attrs={'class': 'form-control'})
        form.fields['year_of_death'].widget = forms.TextInput(attrs={'class': 'form-control'})
        return form

class BookCreateView(PermissionRequiredMixin,CreateView):
    """
    Generic class-based view for creating a book.
    """
    model = Book
    fields = '__all__'
    permission_required = 'book_catalog.add_book'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        author_choices = [(author.id, author) for author in Author.objects.all()]
        saga_choices = [('', '---------')] + [(saga.id, saga) for saga in BookSaga.objects.all()]
        language_choices = [(language.id, language) for language in Language.objects.all()]
        genre_choices = [(genre.id, genre) for genre in Genre.objects.all()]
        form.fields['title'].widget = forms.TextInput(attrs={'class': 'form-control'})
        form.fields['title'].order = 1
        form.fields['author'].widget = forms.Select(attrs={'class': 'form-select'}, choices=author_choices)
        form.fields['author'].order = 2
        form.fields['saga'].widget = forms.Select(attrs={'class': 'form-select'}, choices=saga_choices)
        form.fields['saga'].order = 3
        form.fields['saga_volume'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        form.fields['saga_volume'].order = 4
        form.fields['publish_date'].widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        form.fields['publish_date'].order = 5
        form.fields['summary'].widget = forms.Textarea(attrs={'class': 'form-control'})
        form.fields['summary'].order = 6
        form.fields['isbn'].widget = forms.TextInput(attrs={'class': 'form-control'})
        form.fields['isbn'].order = 7
        form.fields['language'].widget = forms.Select(attrs={'class': 'form-select'}, choices=language_choices)
        form.fields['language'].order = 8
        form.fields['genre'].widget = forms.SelectMultiple(attrs={'class': 'form-select'}, choices=genre_choices)
        form.fields['genre'].order = 9
        form.fields['cover_image'].widget = forms.ClearableFileInput(attrs={'class': 'form-control'})
        form.fields['cover_image'].order = 10
        return form

class BookSagaCreateView(PermissionRequiredMixin,CreateView):
    """
    Generic class-based view for creating an author.
    """
    model = BookSaga
    fields = '__all__'
    permission_required = 'book_catalog.add_booksaga'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authors = Author.objects.all()
        context['authors'] = authors
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        author_choices = [(author.id, author) for author in Author.objects.all()]
        form.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        form.fields['author'].widget = forms.Select(attrs={'class': 'form-select'}, choices=author_choices)
        return form

################# Update Views #################

class AuthorUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Generic class-based view for updating an author.
    """
    model = Author
    fields = ['first_name', 'last_name', 'year_of_birth', 'year_of_death']
    permission_required = 'book_catalog.change_author'
    template_name = 'book_catalog/author_form.html'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        books = author.book_set.all().order_by('saga', 'saga_volume')
        context['books'] = books
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['first_name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        form.fields['last_name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        form.fields['year_of_birth'].widget = forms.TextInput(attrs={'class': 'form-control'})
        form.fields['year_of_death'].widget = forms.TextInput(attrs={'class': 'form-control'})
        return form

    def get_success_url(self):
        return reverse('author-detail', args=[str(self.object.pk)])

class BookUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Generic class-based view for updating a book.
    """
    model = Book
    fields = '__all__'
    permission_required = 'book_catalog.change_book'
    template_name = 'book_catalog/book_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        author_choices = [(author.id, author) for author in Author.objects.all()]
        saga_choices = [(saga.id, saga) for saga in BookSaga.objects.all()]
        language_choices = [(language.id, language) for language in Language.objects.all()]
        genre_choices = [(genre.id, genre) for genre in Genre.objects.all()]
        form.fields['title'].widget = forms.TextInput(attrs={'class': 'form-control'})
        form.fields['title'].order = 1
        form.fields['author'].widget = forms.Select(attrs={'class': 'form-select'}, choices=author_choices)
        form.fields['author'].order = 2
        form.fields['saga'].widget = forms.Select(attrs={'class': 'form-select'}, choices=saga_choices)
        form.fields['saga'].order = 3
        form.fields['saga_volume'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        form.fields['saga_volume'].order = 4
        form.fields['publish_date'].widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        form.fields['publish_date'].order = 5
        form.fields['summary'].widget = forms.Textarea(attrs={'class': 'form-control'})
        form.fields['summary'].order = 6
        form.fields['isbn'].widget = forms.TextInput(attrs={'class': 'form-control'})
        form.fields['isbn'].order = 7
        form.fields['language'].widget = forms.Select(attrs={'class': 'form-select'}, choices=language_choices)
        form.fields['language'].order = 8
        form.fields['genre'].widget = forms.SelectMultiple(attrs={'class': 'form-select'}, choices=genre_choices)
        form.fields['genre'].order = 9
        form.fields['cover_image'].widget = forms.ClearableFileInput(attrs={'class': 'form-control'})
        form.fields['cover_image'].order = 10
        return form

    def get_success_url(self):
        return reverse('book-detail', args=[str(self.object.pk)])

class BookSagaUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Generic class-based view for updating a book saga.
    """
    model = BookSaga
    fields = ['name']
    template_name = 'book_catalog/booksaga_form.html'
    permission_required = 'book_catalog.change_booksaga'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        return form
    def get_success_url(self):
        return reverse('saga-detail', args=[str(self.object.pk)])

class UserBookRelationUpdateView(LoginRequiredMixin, UpdateView):
    """
    Generic class-based view for updating a book saga.
    """
    model = UserBookRelation
    fields = ['status', 'read_date', 'reading_date', 'rate', 'review']
    template_name = 'book_catalog/userbookrelation_form.html'
    success_url = reverse_lazy('my-books')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['status'].widget = forms.Select(attrs={'class': 'form-select'}, choices=UserBookRelation.STATUS_CHOICES)
        form.fields['read_date'].widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        form.fields['reading_date'].widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        form.fields['rate'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        form.fields['review'].widget = forms.Textarea(attrs={'class': 'form-control'})
        return form

################# Delete Views #################

class AuthorDeleteView(PermissionRequiredMixin,DeleteView):
    """
    Generic class-based view for deleting an author.
    """
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'book_catalog.delete_author'

class BookDeleteView(PermissionRequiredMixin,DeleteView):
    """
    Generic class-based view for deleting a book.
    """
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'book_catalog.delete_book'

class BookSagaDeleteView(PermissionRequiredMixin,DeleteView):
    """
    Generic class-based view for deleting a book saga.
    """
    model = BookSaga
    success_url = reverse_lazy('books')
    permission_required = 'book_catalog.delete_booksaga'

################# Form Views #################


@login_required
def change_book_status(request, pk, status: str):
    """
    View function for changing book status.
    """
    book = get_object_or_404(Book, pk=pk)
    relation = UserBookRelation.objects.filter(user = request.user, book = book).first()
    if relation:
        if status == 'd':
            relation.status = None
            relation.read_date = None
            relation.reading_date = None
            relation.save()
        else:
            relation.status = status
            if status == 'r':
                relation.read_date = timezone.now()
            if status == 'i':
                relation.reading_date = timezone.now()
            relation.save()
    elif not relation and status != 'd':
        UserBookRelation.objects.create(user = request.user, book = book, status = status)
    return HttpResponseRedirect(reverse('book-detail', args=[str(pk)]))

# @login_required
# def delete_book_status(request, pk):
#     """
#     View function for changing book status.
#     """
#     book = get_object_or_404(Book, pk=pk)
#     UserBookRelation.objects.filter(user = request.user, book = book).delete()
#     return HttpResponseRedirect(reverse('book-detail', args=[str(pk)]))

@login_required
def change_booksaga_status(request, pk, status: str):
    """
    View function for changing book status.
    """
    booksaga = get_object_or_404(BookSaga, pk=pk)
    for book in booksaga.book_set.all():
        relation = UserBookRelation.objects.filter(user = request.user, book = book).first()
        if relation:
            if status == 'd':
                relation.delete()
            else:
                relation.status = status
                relation.save()
        elif not relation and status != 'd':
            UserBookRelation.objects.create(user = request.user, book = book, status = status)
    return HttpResponseRedirect(reverse('saga-detail', args=[str(pk)]))

def search(request):
    """
    View function for searching books, authors and sagas.
    """
    query = request.GET.get('query')
    book_results = []
    author_results = []
    saga_results = []
    
    if query:
        book_results = Book.objects.filter(title__icontains=query)
        author_results = Author.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
        saga_results = BookSaga.objects.filter(name__icontains=query)
    
    context = {
        'query': query,
        'book_results': book_results,
        'author_results': author_results,
        'saga_results': saga_results,
    }
    
    return render(request, 'search_results.html', context)
