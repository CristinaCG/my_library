from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
from person_catalog.models import Person
from core.models import Genre, Language
# Create your models here.

class Author(Person):
    """ Modelo que representa un autor"""
    bio = models.TextField(null=True, blank=True, verbose_name='Biography')
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this author."""
        return reverse('author-detail', args=[str(self.id)])

class Book(models.Model):
    """ Modelo que representa un libro"""
    title = models.CharField(max_length=255)

    authors = models.ManyToManyField(Author,max_length=255,)

    summary = models.TextField(max_length=2000, help_text='Enter a brief description of the book')

    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    
    language = models.ManyToManyField(Language, max_length=100)

    genre = models.ManyToManyField(Genre)
    
    publication_date = models.DateField()

    page_count = models.IntegerField(null=True, blank=True)

    publisher = models.CharField(max_length=255)

    saga = models.CharField(max_length=255, null=True, blank=True, default='')
    
    volume = models.IntegerField(null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
    
    def display_author(self):
        """Create a string for the Author. This is required to display author in Admin."""
        return ', '.join(f'{author.first_name[0]}. {author.last_name}' for author in self.authors.all()[:3])
    display_author.short_description = 'Author'
    

