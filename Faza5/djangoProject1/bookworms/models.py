from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UsernamesPasswordsManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class UsernamesPasswords(AbstractBaseUser, PermissionsMixin):
    idUser = models.AutoField(primary_key=True)
    username = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=45, unique=True)
    profileImage = models.ImageField(upload_to='images/', default='/images/userProfile.svg')
    last_login = models.DateTimeField(('last login'), blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_query_name="usernamespasswords",
        related_name="usernamespasswords_set",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_query_name="usernamespasswords",
        related_name="usernamespasswords_set",
    )

    objects = UsernamesPasswordsManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'UsernamesPasswords'
class User(models.Model):
    idUser = models.OneToOneField(UsernamesPasswords, on_delete=models.CASCADE, primary_key=True, db_column='idUser')

    class Meta:
        db_table = 'User'



class Reviewer(models.Model):
    idUserRew = models.OneToOneField(UsernamesPasswords, on_delete=models.CASCADE, primary_key=True, db_column='idUserRew')
    bio = models.TextField()
    class Meta:
        db_table = 'Reviewer'

class AuthorShow(models.Model):
    idAuthor = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    bioShow = models.TextField()
    class Meta:
        db_table = 'AuthorShow'

class Author(models.Model):
    idUserAuth = models.OneToOneField(UsernamesPasswords, on_delete=models.CASCADE, primary_key=True, db_column='idUserAuth')
    idAuthor = models.ForeignKey(AuthorShow, on_delete=models.CASCADE, db_column='idAuthor')
    bio = models.TextField(null=True)
    class Meta:
        db_table = 'Author'

class Book(models.Model):
    idBook = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=45)
    genre = models.CharField(max_length=60)
    description = models.TextField()
    coverImage = models.ImageField(upload_to='images/', default='images/userProfile.svg')
    class Meta:
        db_table = 'Book'

class ReadList(models.Model):
    idUser = models.ForeignKey(UsernamesPasswords, on_delete=models.CASCADE, db_column='idUser')
    idBook = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='idBook')
    rating = models.IntegerField(null=True)
    class Meta:
        db_table = 'ReadList'

class WishList(models.Model):
    idUser = models.ForeignKey(UsernamesPasswords, on_delete=models.CASCADE, db_column='idUser')
    idBook = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='idBook')
    class Meta:
        db_table = 'WishList'

class RecommendationList(models.Model):
    idUser = models.ForeignKey(UsernamesPasswords, on_delete=models.CASCADE, db_column='idUser')
    idBook = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='idBook')
    class Meta:
        db_table = 'RecommendationList'

class AuthorWroteBook(models.Model):
    idAuthor = models.ForeignKey(AuthorShow, on_delete=models.CASCADE, db_column='idUser')
    idBook = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='idBook')
    class Meta:
        db_table = 'AuthorWroteBook'

class Reviews(models.Model):
    idReview = models.AutoField(primary_key=True)
    reviewText = models.TextField()
    idBook = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='idBook')
    idUser = models.ForeignKey(UsernamesPasswords, on_delete=models.CASCADE, db_column='idUser')
    class Meta:
        db_table = 'Reviews'

class Badge(models.Model):
    idBadge = models.AutoField(primary_key=True)
    description = models.TextField()
    class Meta:
        db_table = 'Badge'

class HasBadge(models.Model):
    idBadge = models.ForeignKey(Badge, on_delete=models.CASCADE, db_column='idBadge')
    idUser = models.ForeignKey(UsernamesPasswords, on_delete=models.CASCADE, db_column='idUser')

    class Meta:
        unique_together = (('idBadge', 'idUser'),)
        db_table = 'HasBadge'
class Challenge(models.Model):
    idChallenge = models.AutoField(primary_key=True)
    status = models.CharField(max_length=45)
    idBadge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    startDate = models.DateField()
    endDate = models.DateField()
    class Meta:
        db_table = 'Challenge'

class ChallengeBooks(models.Model):
    idChallenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    idBook = models.ForeignKey(Book, on_delete=models.CASCADE)
    class Meta:
        db_table = 'ChallengeBooks'

class Achievement(models.Model):
    idAchievement = models.AutoField(primary_key=True)
    idBadge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    numberOfBooks = models.IntegerField()
    class Meta:
        db_table = 'Achievement'

class Administrator(models.Model):
    idAdmin = models.AutoField(primary_key=True)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    class Meta:
        db_table = 'Administrator'

class Request(models.Model):
    idRequest = models.AutoField(primary_key=True)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE, db_column='idUser')
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    class Meta:
        db_table = 'Request'