from django.contrib import admin
from .models import Author, Book, Genre, Language, BookSaga, UserBookRelation

admin.site.register(Genre)
admin.site.register(Language)

class BookInline(admin.TabularInline):
    """
    Defines format of inline book insertion (used in AuthorAdmin)
    """
    model = Book
    extra = 1
    fields = ['title', 'publish_date', 'saga_volume']

class AuthorAdmin(admin.ModelAdmin):
    """
    Administration object for Author models.
    """
    inlines = [BookInline]

class BookSagaAdmin(admin.ModelAdmin):
    """
    Administration object for BookSaga models.
    """
    inlines = [BookInline]

admin.site.register(BookSaga, BookSagaAdmin)

admin.site.register(Author, AuthorAdmin)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Administration object for Book models.
    """
    list_display = ('display_title', 'display_author', 'publish_date')
    list_filter = ('author', 'saga')


@admin.register(UserBookRelation)
class UserBookRelationAdmin(admin.ModelAdmin):
    """
    Administration object for UserBookRelation models.
    """
    list_display = ('book', 'user', 'status', 'rating', 'reading_date', 'read_date')
    list_filter = ('user', 'status')
    fields = ['user', 'book', 'status', 'rating', 'reading_date', 'read_date', 'review']
