from django.db import models

from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager


class CustomProfileManager(BaseUserManager):

    def create_user(self, email, username, string_id, password=None, description=None, realname=None, profile_img=None):
        user = self.model(email=email, username=username, password=password)
        user.username = username
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.model(email=email, username=username, password=password)
        user.username = username
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username_):
        print(username_)
        return self.get(username=username_)


class Profile(AbstractBaseUser, PermissionsMixin):
    objects = CustomProfileManager()

    string_id = models.CharField(max_length=100, unique=True, primary_key=True)

    email = models.EmailField(unique=True, default=None)
    password = models.CharField(max_length=100)

    username = models.CharField(max_length=100, unique=True)
    realname = models.CharField(max_length=30, blank=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    description = models.TextField(max_length=200)

    subscriptions = models.ForeignKey('self', related_name='users_subscr', on_delete=models.CASCADE, null=True,
                                      blank=True)
    followers = models.ForeignKey('self', related_name='users_followers', on_delete=models.CASCADE, null=True,
                                  blank=True)

    profile_img = models.ImageField()

    marks = models.ManyToManyField('Mark', related_name='users', blank=True)

    registration_date = models.DateTimeField(auto_now_add=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Mark(models.Model):

    lon = models.FloatField()
    lat = models.FloatField()
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.users