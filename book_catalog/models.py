from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns

# Create your models here.
class Genre(models.Model):
    """ Modelo que representa el género literario de un libro"""
    name = models.CharField(max_length=255, help_text='Enter a book genre (e.g. Science Fiction, Poetry, Fantasy etc.)')

    def __str__(self):
        return self.name

class Language(models.Model):
    """ Modelo que representa el idioma de un libro"""
    name = models.CharField(max_length=255, help_text='Enter the book\'s language (e.g. English, French, Spanish etc.)')

    def __str__(self):
        return self.name
    
class Book(models.Model):
    """ Modelo que representa un libro"""
    title = models.CharField(max_length=255)

    authors = models.ManyToManyField('Author',max_length=255)
    # ManyToManyField used because genre can contain many books. Books can cover many genres.

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')

    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    
    language = models.ManyToManyField(Language, max_length=100)

    genre = models.ManyToManyField(Genre)
    
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    publication_date = models.DateField()

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
    
class Author(models.Model):
    """ Modelo que representa un autor"""
    first_name = models.CharField(max_length=255)

    last_name = models.CharField(max_length=255)

    birth_date = models.DateField()

    death_date = models.DateField(null=True, blank=True)

    books = models.ManyToManyField(Book) 

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this author."""
        return reverse('author-detail', args=[str(self.id)])
