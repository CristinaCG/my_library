from django.contrib import admin
from .models import Author, Book, Genre, Language, BookState, BookSaga

# Register your models here.
# admin.site.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'year_of_birth', 'year_of_death')

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

# admin.site.register(Book)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_author', 'publish_date')
    list_filter = ('author', 'saga')

# admin.site.register(BookState)
@admin.register(BookState)
class BookStateAdmin(admin.ModelAdmin):
    pass

admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(BookSaga)