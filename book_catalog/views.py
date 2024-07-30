from typing import Any
from operator import and_
from functools import reduce
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django import forms
from .models import Author, Book, BookSaga, UserBookRelation, Language, Genre


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
        # 'average_books_per_month': average_books_per_month,
    }
    if request.user.is_authenticated:
        books_reading_id = UserBookRelation.objects.filter(
            user=request.user, status='i').order_by('-id')[:3]
        books_reading = [Book.objects.get(pk=book.book_id) for book in books_reading_id]
        context['my_books_reading'] = books_reading

        books_read_id = UserBookRelation.objects.filter(
            user=request.user, status='r').order_by('-id')
        context['my_books_read'] = len(books_read_id)

        reading_id = UserBookRelation.objects.filter(
            user=request.user, status='r', read_date__year=timezone.now().year)
        context['my_books_this_year'] = len(reading_id)

    return render(request, 'index_book.html', context = context,)

################# List Views #################

class BookListView(ListView):
    """
    Generic class-based view listing books.
    """
    model = Book
    template_name = 'book_catalog/book_list.html'

    def get_context_data(self, **kwargs):
        """
        Recent book list
        """
        context = super().get_context_data(**kwargs)
        context["recent_books"] = Book.objects.all().order_by('-publish_date')[:5]
        return context

class AuthorListView(ListView):
    """
    Generic class-based view listing authors.
    """
    model = Author
    template_name = 'book_catalog/author_list.html'

    def get_context_data(self, **kwargs: Any):
        """
        Obtain an author list of authors that has books published recently
        """
        context = super().get_context_data(**kwargs)
        context["recent_books"] = Book.objects.all().order_by('-publish_date')[:5]
        return context

class UserBookRelationListView(LoginRequiredMixin, ListView):
    """
    Generic class-based view listing books of the current user.
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = UserBookRelation
    template_name = 'book_catalog/userbookrelation_list.html'
    # paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    # template_name ='templates/book_catalog/userbookrelation_list.html'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["recent_books"] = Book.objects.all().order_by('-publish_date')[:5]
        return context

################# Detail Views #################

class BookDetailView(LoginRequiredMixin, DetailView):
    """
    Generic class-based view detail of a book.
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Book
    template_name = 'book_catalog/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        user_book_relation = UserBookRelation.objects.filter(
            book=book, user=self.request.user).first()
        context['my_book'] = user_book_relation
        context['average_rating'] = book.average_rating()
        context['average_rating_over_100'] = int(
            context['average_rating']*20) if context['average_rating'] else 0
        context['total_ratings'] = book.number_of_ratings()
        context['rating_range'] = range(5, 0, -1)
        context['total_reviews'] = book.number_of_reviews()
        reviews = book.get_reviews()
        if reviews:
            for review in reviews:
                review.user.review_count = UserBookRelation.objects.filter(
                    user=self.request.user).exclude(review__isnull=True).values_list('review').count()
                review.user.average_rating = UserBookRelation.objects.filter(
                    user=self.request.user).exclude(rating__isnull=True).values_list('rating').count()
                review.rating_over_100 = int(review.rating*20) if review.rating else 0
        context['book_reviews'] = reviews

        # context['user_id'] = self.request.user.id
        return context

class AuthorDetailView(LoginRequiredMixin, DetailView):
    """
    Generic class-based view detail of an author.
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Author
    template_name = 'book_catalog/author_detail.html'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        books = author.book_set.all().order_by('saga', 'saga_volume')
        context['books'] = books
        context['average_rating'] = author.average_rating()
        context['average_rating_over_100'] = int(
            context['average_rating']*20) if context['average_rating'] else 0
        context['book_list'] = Book.objects.filter(author=author)
        context['total_ratings'] = author.number_of_ratings()
        context['total_reviews'] = author.number_of_reviews()
        return context

class BookSagaDetailView(LoginRequiredMixin, DetailView):
    """
    Generic class-based view detail of a book saga.
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = BookSaga
    template_name = 'book_catalog/booksaga_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        saga = self.get_object()
        books = saga.book_set.all().order_by('saga_volume')
        relations = [0]*len(books)
        for i, book in enumerate(books):
            relation = UserBookRelation.objects.filter(book=book, user=self.request.user).first()
            if relation:
                if relation.status == 'r':
                    relations[i] = 3
                    book.status = 'r'
                if relation.status == 'i':
                    relations[i] = 2
                    book.status = 'i'
                if relation.status == 't':
                    relations[i] = 1
                    book.status = 't'
            # print(relations)
        if sum(relations) == 3*len(saga.book_set.all()):
            context['user_saga_relation'] = 'r'
        elif sum(relations) >= len(saga.book_set.all())+1+2:
            context['user_saga_relation'] = 'i'
        elif sum(relations) >= len(saga.book_set.all()):
            context['user_saga_relation'] = 't'
        context['books'] = books
        context['average_rating'] = saga.average_rating()
        context['average_rating_over_100'] = int(
            context['average_rating']*20) if context['average_rating'] else 0
        context['book_list'] = Book.objects.filter(saga=saga)
        context['total_ratings'] = saga.number_of_ratings()
        context['total_reviews'] = saga.number_of_reviews()
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
        form.fields['biography'].widget = forms.Textarea(attrs={'class': 'form-control'})
        form.fields['photo'].widget = forms.ClearableFileInput(attrs={'class': 'form-control'})
        form.fields['social_media'].widget = forms.URLInput(attrs={'class': 'form-control'})
        return form

class BookCreateView(PermissionRequiredMixin,CreateView):
    """
    Generic class-based view for creating a book.
    """
    model = Book
    fields = ['title', 'author', 'saga', 'saga_volume', 'publish_date', 'summary', 'isbn', 'language', 'genre', 'cover_image']
    permission_required = 'book_catalog.add_book'
    template_name = 'book_catalog/book_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        author_choices = [(author.id, author) for author in Author.objects.all()]
        saga_choices = [('', '---------')] + [(saga.id, saga) for saga in BookSaga.objects.all()]
        language_choices = [(language.id, language) for language in Language.objects.all()]
        genre_choices = [(genre.id, genre) for genre in Genre.objects.all()]

        form.fields['title'].widget = forms.TextInput(attrs={'class': 'form-control'})
        form.fields['author'].widget = forms.Select(attrs={'class': 'select2 form-select'}, choices=author_choices)
        form.fields['saga'].widget = forms.Select(attrs={'class': 'select2 form-select'}, choices=saga_choices)
        form.fields['saga_volume'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        form.fields['publish_date'].widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        form.fields['summary'].widget = forms.Textarea(attrs={'class': 'form-control'})
        form.fields['isbn'].widget = forms.TextInput(attrs={'class': 'form-control'})
        form.fields['language'].widget = forms.Select(attrs={'class': 'select2 form-select'}, choices=language_choices)
        form.fields['genre'].widget = forms.SelectMultiple(attrs={'class': 'select2 form-select'}, choices=genre_choices)
        form.fields['cover_image'].widget = forms.ClearableFileInput(attrs={'class': 'form-control'})
        return form

class BookSagaCreateView(PermissionRequiredMixin,CreateView):
    """
    Generic class-based view for creating an author.
    """
    model = BookSaga
    fields = '__all__'
    permission_required = 'book_catalog.add_booksaga'
    template_name = 'book_catalog/booksaga_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authors = Author.objects.all()
        context['authors'] = authors
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        author_choices = [(author.id, author) for author in Author.objects.all()]
        form.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        form.fields['author'].widget = forms.Select(attrs={'class': 'form-select  select2'}, choices=author_choices)
        form.fields['description'].widget = forms.Textarea(attrs={'class': 'form-control'})
        return form

################# Update Views #################

class AuthorUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Generic class-based view for updating an author.
    """
    model = Author
    fields = ['first_name', 'social_media', 'last_name', 'year_of_birth', 'year_of_death', 'biography', 'photo']
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
        form.fields['biography'].widget = forms.Textarea(attrs={'class': 'form-control'})
        form.fields['photo'].widget = forms.ClearableFileInput(attrs={'class': 'form-control'})
        form.fields['social_media'].widget = forms.URLInput(attrs={'class': 'form-control'})
        return form

    def get_success_url(self):
        return reverse('author-detail', args=[str(self.object.pk)])

class BookUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Generic class-based view for updating a book.
    """
    model = Book
    fields = ['title', 'author', 'saga', 'saga_volume', 'publish_date', 'summary', 'isbn', 'language', 'genre', 'cover_image']
    permission_required = 'book_catalog.change_book'
    template_name = 'book_catalog/book_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        author_choices = [(author.id, author) for author in Author.objects.all()]
        saga_choices = [(saga.id, saga) for saga in BookSaga.objects.all()]
        saga_choices = [('', '---------')] + saga_choices
        language_choices = [(language.id, language) for language in Language.objects.all()]
        genre_choices = [(genre.id, genre) for genre in Genre.objects.all()]
        form.fields['title'].widget = forms.TextInput(attrs={'class': 'form-control'})
        form.fields['author'].widget = forms.Select(attrs={'class': 'select2 form-select'}, choices=author_choices)
        form.fields['saga'].widget = forms.Select(attrs={'class': 'select2 form-select'}, choices=saga_choices)
        form.fields['saga_volume'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        form.fields['publish_date'].widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        form.fields['summary'].widget = forms.Textarea(attrs={'class': 'form-control'})
        form.fields['isbn'].widget = forms.TextInput(attrs={'class': 'form-control'})
        form.fields['language'].widget = forms.Select(attrs={'class': 'select2 form-select'}, choices=language_choices)
        form.fields['genre'].widget = forms.SelectMultiple(attrs={'class': 'select2 form-select'}, choices=genre_choices)
        form.fields['cover_image'].widget = forms.ClearableFileInput(attrs={'class': 'form-control'})
        return form

    def get_success_url(self):
        return reverse('book-detail', args=[str(self.object.pk)])

class BookSagaUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Generic class-based view for updating a book saga.
    """
    model = BookSaga
    fields = ['name', 'author', 'description']
    template_name = 'book_catalog/booksaga_form.html'
    permission_required = 'book_catalog.change_booksaga'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        author_choices = [(author.id, author) for author in Author.objects.all()]
        form.fields['author'].widget = forms.Select(attrs={'class': 'select2 form-select'}, choices=author_choices)
        form.fields['description'].widget = forms.Textarea(attrs={'class': 'form-control'})
        return form

    def get_success_url(self):
        return reverse('saga-detail', args=[str(self.object.pk)])

class UserBookRelationUpdateView(LoginRequiredMixin, UpdateView):
    """
    Generic class-based view for updating a book saga.
    """
    model = UserBookRelation
    fields = ['status', 'reading_date', 'read_date',  'rating', 'review']
    template_name = 'book_catalog/userbookrelation_form.html'

    def get_success_url(self):
        return reverse('book-detail', args=[str(self.object.book.pk)])

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['status'].widget = forms.Select(attrs={'class': 'select2 form-select'}, choices=UserBookRelation.STATUS_CHOICES)
        form.fields['reading_date'].widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        form.fields['reading_date'].label = 'You started reading this book on'
        form.fields['read_date'].widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        form.fields['read_date'].label = 'You finished reading this book on'
        form.fields['rating'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        form.fields['review'].widget = forms.Textarea(attrs={'class': 'form-control'})
        return form

    def form_valid(self, form):
        relation = form.save(commit=False)
        if relation.status == 'r' and relation.read_date is None:
            relation.read_date = timezone.now().date()
        elif relation.status == 'i' and relation.reading_date is None:
            relation.reading_date = timezone.now().date()
        if relation.review and relation.review_date is None:
            relation.review_date = timezone.now().date()
        return super().form_valid(form)

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
def change_book_status(request, pk: int, status: str):
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
            if relation.status == 'r' and relation.read_date is None:
                relation.read_date = timezone.now().date()
            elif relation.status == 'i' and relation.reading_date is None:
                relation.reading_date = timezone.now().date()
            relation.save()
    elif not relation and status != 'd':
        relation = UserBookRelation.objects.create(user = request.user, book = book, status = status)
        if relation.status == 'r' and relation.read_date is None:
            relation.read_date = timezone.now().date()
        elif relation.status == 'i' and relation.reading_date is None:
            relation.reading_date = timezone.now().date()
        relation.save()
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
                relation.status = None
                relation.save()
            else:
                relation.status = status
                relation.save()
        elif not relation and status != 'd':
            UserBookRelation.objects.create(user = request.user, book = book, status = status)
    return HttpResponseRedirect(reverse('saga-detail', args=[str(pk)]))


def search(request):
    """
    View function for searching books.
    """
    query = request.GET.get('query')
    if query:
        query_parts = query.split()
        author_conditions = [Q(first_name__icontains=part) | Q(last_name__icontains=part) for part in query_parts]
        combined_author_conditions = reduce(and_, author_conditions)
        author_results = Author.objects.filter(combined_author_conditions)

        book_results = Book.objects.filter(title__icontains=query)
        author_books = Book.objects.filter(author__in=author_results)

        saga_books = Book.objects.filter(saga__name__icontains=query)
        combined_results = book_results | author_books | saga_books
        combined_results = combined_results.distinct()
    else:
        combined_results = Book.objects.all()

    for book in combined_results:
        status = UserBookRelation.objects.filter(user=request.user, book=book).first()
        book.status = status.display_status if status else ''
    context = {
        'query': query,
        'book_results': combined_results,
    }
    return render(request, 'search_results.html', context)

def rating_book(request, pk, rating: int):
    """
    View function for updating book rating.
    """
    if rating >= 0 and rating <= 5:
        book = get_object_or_404(Book, pk=pk)
        relation = UserBookRelation.objects.filter(user = request.user, book = book).first()
        if relation:
            if rating == relation.rating:
                relation.rating = None
            else:
                relation.rating = rating
            relation.save()
        else:
            UserBookRelation.objects.create(user = request.user, book = book, rating = rating)
    return HttpResponseRedirect(reverse('book-detail', args=[str(pk)]))
