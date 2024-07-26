from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Genre(models.Model):
    """
    Model representing a book genre (e.g. Science Fiction, Non Fiction).
    """
    name = models.CharField(max_length=200,
                            help_text='Enter a book genre (e.g. Science Fiction,'
                            'French Poetry etc.)')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return str(self.name)

    def clean(self):
        """
        Check if the genre is valid
        """
        if self.name is not None:
            if self.name == "":
                raise ValidationError("Genre cannot be empty.")
            if len(self.name) > 200:
                raise ValidationError("Genre is too long, maximum length is 200 characters")

    def save(self, *args, **kwargs):
        """
        Save the genre in the data base
        """
        # self.clean()
        self.full_clean()
        super().save(*args, **kwargs)

class Language(models.Model):
    """
    Model representing a Language (e.g. English, French, Japanese, etc.)
    """
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. "
                            "English, French, Japanese etc.)")

    def __str__(self):
        """
        String for representing the Model object.
        """
        return str(self.name)

    def clean(self):
        """
        Check if the language is valid
        """
        if self.name == "":
            raise ValidationError("Language cannot be empty.")
        if len(self.name) > 200:
            raise ValidationError("Language is too long, maximum length is "
                                  "200 characters.")
    
    def save(self, *args, **kwargs):
        """
        Save the language in the data base
        """
        # self.clean()
        self.full_clean()
        super().save(*args, **kwargs)

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
    title = models.CharField(max_length=200, help_text='Inserte el título del libro.')
    saga = models.ForeignKey('BookSaga', on_delete=models.PROTECT, null=True, blank=True)
    saga_volume = models.IntegerField(null=True, blank=True)
    author = models.ForeignKey('Author', on_delete=models.PROTECT, null=False)
    publish_date = models.DateField(null=True, blank=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book', null=True, blank=True)
    isbn = models.CharField(max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>', null=True, blank=True)
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, blank=True)
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)

    class Meta:
        """
        Metadata for the model.
        """
        ordering = ['title', 'author']
        unique_together = ('title', 'author')
        constraints = [
            models.UniqueConstraint(fields=['saga', 'saga_volume'], name='unique_volume_in_saga')
        ]

    def __str__(self):
        """
        String for representing the Model object.
        """
        return str(self.title)

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
        if (self.saga is None) and (self.saga_volume is not None):
            raise ValidationError("Saga cannot be empty if saga volume is set")
        if self.title == "":
            raise ValidationError("Title cannot be empty")
        if len(self.title) > 200:
            raise ValidationError("Title is too long, maximum length is 200 characters")
        if self.publish_date is not None:
            if self.publish_date > timezone.now().date():
                raise ValidationError("Publish date cannot be in the future")
        if self.saga is not None:
            if self.saga.author != self.author:
                raise ValidationError("Saga author must be the same as the book author")
        if (self.isbn is not None) and (len(self.isbn) != 13):
            raise ValidationError(f"ISBN must have 13 characters, current length is {len(self.isbn)}")
        if (self.summary is not None) and (len(self.summary) > 1000):
            raise ValidationError("Summary is too long, maximum length is 1000 characters")


    def save(self, *args, **kwargs):
        # self.clean()
        self.full_clean()
        super().save(*args, **kwargs)

class UserBookRelation(models.Model):
    """
    Model representing a book state (e.g. read, to read, reading).
    """
    STATUS_CHOICES = (
        ('r', 'Read'),
        ('t', 'To read'),
        ('i', 'Reading'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES,
                              help_text = "Estado actual del libro")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book',)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return f'{self.user.username} ({self.book.title})'

    class Meta:
        """
        Metadata for the model.
        """
        # Para evitar que se puedan tener en la base de datos más de una relación entre un usuario y el mismo libro
        unique_together = ('user', 'book')

    def clean(self):
        if self.status not in ['r', 't', 'i']:
            raise ValidationError("Invalid status, must be 'r', 't' or 'i'")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def display_status(self):
        if self.status == 'r':
            return "Read"
        if self.status == 't':
            return "To Read"
        if self.status == 'i':
            return "Reading"

class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    year_of_birth = models.IntegerField(null = True, blank = True)
    year_of_death = models.IntegerField(null = True, blank = True)

    class Meta:
        """
        Metadata for the model.
        """
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
        if len(self.first_name) == 0:
            raise ValidationError("First name cannot be empty")
        if len(self.last_name) == 0:
            raise ValidationError("Last name cannot be empty")
        if len(self.first_name) > 100:
            raise ValidationError("First name is too long, maximum length is 100 characters")
        if len(self.last_name) > 100:
            raise ValidationError("Last name is too long, maximum length is 100 characters")

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
        return str(self.name)

    def get_absolute_url(self):
        """
        Returns the url to access a particular saga instance.
        """
        return reverse('saga-detail', args=[str(self.id)])

    def clean(self):
        if self.name is not None:
            if len(self.name) == 0:
                raise ValidationError("Saga cannot be empty.")
            if len(self.name) > 200:
                raise ValidationError("Saga name is too long, maximum length is 200 characters.")

    def save(self, *args, **kwargs):
        # self.clean()
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('name', 'author')
