from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from team.models import Team
from team.constants import DEFAULT_TEAM_NAME
from django.core.exceptions import ObjectDoesNotExist


class CustomUserManager(BaseUserManager):
    def _validate_parameters(self, email, password, extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))

        if not password:
            raise ValueError(_('Password filed must be set'))

        username = extra_fields.get('username')
        if not username:
            raise ValueError(_('Username is required'))

        team = extra_fields.get('team')
        if not team or not isinstance(team, Team):
            team_instance = Team.objects.get(name=DEFAULT_TEAM_NAME)
            extra_fields['team'] = team_instance

    
    def create_user(self, email, password=None, **extra_fields):
        self._validate_parameters(email, password, extra_fields)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        self._validate_parameters(email, password, extra_fields)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    '''
    This attributes are given by superclasses
    password 
    is_superuser
    last_login
    '''
    username = models.CharField(_("username"), max_length=64, unique=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        null=False,
        blank=False
    ) 
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    first_name = models.CharField(_('first name'), max_length=30, null=False, blank=False)
    last_name = models.CharField(_('last name'), max_length=30, null=False, blank=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username

