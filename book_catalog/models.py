from django.db import models
import os
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator


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
    title = models.CharField(max_length=200,)
    saga = models.ForeignKey('BookSaga', on_delete=models.CASCADE, null=True, blank=True)
    saga_volume = models.IntegerField(null=True, blank=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, null=False)
    publish_date = models.DateField(null=True, blank=True)
    summary = models.TextField(max_length=1000, null=True, blank=True)
    isbn = models.CharField(max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>', null=True, blank=True)
    genre = models.ManyToManyField(Genre, )
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

    def number_of_ratings(self):
        ratings = UserBookRelation.objects.filter(book=self).values_list('rating')
        ratings = [rating[0] for rating in ratings if rating[0] is not None]
        return len(ratings)

    def number_of_reviews(self):
        reviews = UserBookRelation.objects.filter(book=self).values_list('review')
        reviews = [review[0] for review in reviews if review[0] is not None]
        return len(reviews)

    def average_rating(self):
        """
        Returns the average rating of the book.
        """
        ratings = UserBookRelation.objects.filter(book=self).values_list('rating')
        ratings = [rating[0] for rating in ratings if rating[0] is not None]
        if len(ratings)>0:
            return sum(ratings) / len(ratings)
        return None

    def get_reviews(self):
        reviews = UserBookRelation.objects.filter(book=self).filter(review__isnull=False).order_by('-review_date')
        reviews = [review for review in reviews if review.review not in (None, '')]
        if reviews:
            return reviews
        return None

    def clean(self):
        if (self.saga is not None) and (self.saga_volume is None):
            raise ValidationError("Saga volume cannot be empty if saga is set.")
        if (self.saga is None) and (self.saga_volume is not None):
            raise ValidationError("Saga cannot be empty if saga volume is set.")
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
        # para la imagen:
        # if self.cover_image is not None:
        #     if not os.path.exists(self.cover_image):
        #         raise ValidationError("Image file does not exist")
        #     if self.cover_image.size > 2*1024*1024:
        #         raise ValidationError("Image file too large ( > 2mb )")
        #     if self.cover_image.file.content_type not in ['image/jpeg', 'image/png']:
        #         raise ValidationError("Image file must be JPEG or PNG")
            


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
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book',)
    reading_date = models.DateField(null=True, blank=True)
    read_date = models.DateField(null=True, blank=True)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)  # Por ejemplo, 1 a 5 estrellas
    review = models.TextField(max_length=1000, null=True, blank=True)
    review_date = models.DateField(null=True, blank=True)

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
        if self.status not in ['r', 't', 'i', None]:
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
    photo = models.ImageField(upload_to='authors/', null=True, blank=True)
    social_media = models.URLField(max_length=200, null=True, blank=True)
    biography = models.TextField(max_length=1000, null=True, blank=True)

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

    def average_rating(self):
        """
        Returns the average rating of the author.
        """
        books = Book.objects.filter(author=self)
        ratings = [book.average_rating() for book in books if book.average_rating() is not None]
        if ratings:
            return sum(ratings) / len(ratings)
        return None

    def number_of_ratings(self):
        books = Book.objects.filter(author=self)
        ratings = [book.number_of_ratings() for book in books]
        return sum(ratings)

    def number_of_reviews(self):
        books = Book.objects.filter(author=self)
        reviews = [book.number_of_reviews() for book in books]
        return sum(reviews)

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
    name = models.CharField(max_length=200,)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='saga', null = False)
    description = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return str(self.name)

    def average_rating(self):
        """
        Returns the average rating of the author.
        """
        books = Book.objects.filter(saga=self)
        ratings = [book.average_rating() for book in books if book.average_rating() is not None]
        if ratings:
            return sum(ratings) / len(ratings)
        return None

    def average_rating_over_100(self):
        """
        Returns the average rating of the author over 100.
        """
        return self.average_rating()*20

    def number_of_ratings(self):
        books = Book.objects.filter(saga=self)
        ratings = [book.number_of_ratings() for book in books]
        return sum(ratings)

    def number_of_reviews(self):
        books = Book.objects.filter(saga=self)
        reviews = [book.number_of_reviews() for book in books]
        return sum(reviews)

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
