from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid

# Create your models here.
class Genre(models.Model):
    """
    Model representing a book genre (e.g. Science Fiction, Non Fiction).
    """
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction, French Poetry etc.)')
    
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name

class Language(models.Model):
    """
    Model representing a Language (e.g. English, French, Japanese, etc.)
    """
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular language instance.
        """
        return reverse('language-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                models.functions.Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message = "Language already exists (case insensitive match)"
            )
        ]

class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """
    title = models.CharField(max_length=200)
    saga = models.ForeignKey('BookSaga', on_delete=models.PROTECT, null=True, blank=True)
    saga_volume = models.IntegerField(null=True, blank=True)
    author = models.ForeignKey('Author', on_delete=models.PROTECT, null=False)
    # ForeignKey, ya que un libro tiene un solo autor, pero el mismo autor puede haber escrito muchos libros.
    # 'Author' es un string, en vez de un objeto, porque la clase Author aún no ha sido declarada.
    publish_date = models.DateField(null=True, blank=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book', null=True, blank=True)
    isbn = models.CharField(max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>', null=True, blank=True)
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    # ManyToManyField, porque un género puede contener muchos libros y un libro puede cubrir varios géneros.
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['title', 'author']
        constraints = [
            models.UniqueConstraint(fields=['saga', 'saga_volume'], name='unique_volume_in_saga')
        ]

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this book.
        """
        return reverse('book-detail', args=[str(self.id)])
    
    def display_author(self):
        """
        Creates a string for the Author. This is required to display author in Admin.
        """
        return f"{self.author.first_name[0]}. {self.author.last_name}"

    def display_title(self):
        """
        Creates a string for the Book. This is required to display book in Admin.
        """
        if self.saga is not None:
            return f"{self.title} ({self.saga.name}, #{self.saga_volume})"
        else:
            return f"{self.title}"

    def clean(self):
        if (self.saga is not None) and (self.saga_volume is None):
            raise ValidationError("Saga volume cannot be empty if saga is set")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
            
class BookState(models.Model):
    """
    Model representing a book state (e.g. read, to read, reading).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book state')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    state = (
        ('r', 'Read'),
        ('t', 'To read'),
        ('i', 'Reading'),
    )
    def __str__(self):
        """
        String for representing the Model object.
        """
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    year_of_birth = models.IntegerField(null = True, blank = True)
    year_of_death = models.IntegerField(null = True, blank = True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        """
        String for representing the Model object.
        """
        return f'{self.first_name} {self.last_name}'

    def _check_year_of_birth(self):
        """
        Check if year of birth is in the future.
        """
        current_year = timezone.now().year
        if self.year_of_birth > current_year:
            raise ValidationError("Year of birth cannot be in the future")
        if self.year_of_birth < 0:
            raise ValidationError("Year of birth cannot be negative")

    def _check_year_of_death(self):
        """
        Check if year of death is in the future.
        """
        current_year = timezone.now().year
        if self.year_of_death > current_year:
            raise ValidationError("Year of death cannot be in the future")
        if self.year_of_death < 0:
            raise ValidationError("Year of death cannot be negative")

    def clean(self):
        if self.year_of_birth is not None:
            self._check_year_of_birth()
        if self.year_of_death is not None:
            self._check_year_of_death()
        if self.year_of_birth and self.year_of_death is not None:
            if self.year_of_birth > self.year_of_death:
                raise ValidationError("Year of birth cannot be after year of death")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class BookSaga(models.Model):
    """
    Model representing a book saga (e.g. Harry Potter, The Lord of the Rings).
    """
    name = models.CharField(max_length=200, help_text='Enter the name of the saga')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='saga', null = False)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular saga instance.
        """
        return reverse('saga-detail', args=[str(self.id)])