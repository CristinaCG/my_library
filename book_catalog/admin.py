from django.contrib import admin
from .models import Book, Author
from core.models import Genre, Language

class BookInline(admin.TabularInline):
    model = Book.authors.through
    extra = 1

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'birth_year')
    fields = ['first_name', 'last_name', ('birth_year', 'death_date'), 'birth_place', 'bio']
    inlines = [BookInline]

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_author', 'saga', 'publication_date')
    list_filter = ('authors','saga', 'publication_date')
    inlines = [BookInline]

admin.site.register(Book,BookAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Language)