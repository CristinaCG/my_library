from django.contrib import admin
from .models import Author, Book, Genre, Language, BookSaga, UserBookRelation

admin.site.register(Genre)
admin.site.register(Language)

class BookInline(admin.TabularInline):  # o puedes usar admin.StackedInline para un diseño diferente
    model = Book
    extra = 1
    fields = ['title', 'publish_date', 'saga_volume']

# admin.site.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'year_of_birth', 'year_of_death')
    fields = [('first_name', 'last_name'), ('year_of_birth', 'year_of_death')]
    # Para poder relacionar libros con autores en la página del autor:
    inlines = [BookInline]

class BookSagaAdmin(admin.ModelAdmin):
    inlines = [BookInline]

admin.site.register(BookSaga, BookSagaAdmin)

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

# admin.site.register(Book)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('display_title', 'display_author', 'publish_date')
    list_filter = ('author', 'saga')
    fields = ['title', 'author', ('saga', 'saga_volume'), 'cover_image', 'publish_date', 'summary', 'language', 'genre', 'isbn']


# admin.site.register(BookState)
@admin.register(UserBookRelation)
class UserBookRelationAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'status', 'reading_date', 'read_date')
    list_filter = ('user', 'status')
    fields = ['user', 'book', 'status']

