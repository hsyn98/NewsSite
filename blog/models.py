from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from multiselectfield import MultiSelectField
CATEGORIES = ((1, 'Business'),
              (2, 'Entertainment'),
              (3, 'General'),
              (4, 'Health'),
              (5, 'Science'),
              (6, 'Sports'),
              (7, 'Technology'))


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, null=True)
    description = models.TextField()
    url = models.URLField()
    image_url = models.URLField(default='none', null=True)
    publish_date = models.DateTimeField()
    content = models.TextField(null=True)
    category = models.TextField(null=True)

    def __str__(self):
       return self.title


class MyUserManager(BaseUserManager):
    def create_user(self, email, user_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not user_name:
            raise ValueError('Users mush have an User name')
        user = self.model(email=self.normalize_email(email), user_name=user_name, )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name, password):
        user = self.create_user(email, password=password, user_name=user_name,)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=False,
    )
    user_name = models.fields.CharField(unique=True, null=False, max_length=255,)
    date_of_birth = models.DateField(null=True)
    first_name = models.CharField(null=True, max_length=30, blank=True)
    last_name = models.CharField(null=True, max_length=30, blank=True)
    interest = MultiSelectField(null=True, max_length=50, blank=False, choices=CATEGORIES)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    def get_full_name(self):
        return self.user_name

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):

        return True

    @property
    def is_staff(self):
        return self.is_admin
