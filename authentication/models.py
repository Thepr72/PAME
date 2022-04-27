from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password):
        """
        Creates a superuser using the create_user function.
        """
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.profile_type = 0
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):

	TYPE = (
		(0, 'Administrador'),
		(1, 'Profesor'),
		(2, 'Alumno'),
	)

	username = models.CharField(max_length=100, unique=True)
	email = models.EmailField(_('Correo'), unique=True)
	first_name = models.CharField(_('Nombre(s)'), max_length=30, blank=True, null=True)
	last_name = models.CharField(_('Apellido(s)'), max_length=30, blank=True, null=True)
	date_joined = models.DateTimeField(_('Fecha de registro'), auto_now_add=True)
	is_staff = models.BooleanField(
            _('administrativo'),
            default=False,
            help_text=_(
                'Designates whether the user can log into this admin site.'),
        )
	is_active = models.BooleanField(
            _('Activo'),
            default=True,
            help_text=_(
                'Designates whether this user should be treated as active. '
                'Unselect this instead of deleting accounts.'
            )
        )
	is_admin = models.BooleanField(
            _('Administrador'),
            default=False,
            help_text=_(
                'Designates whether the user is an admin in the platform. '
                "Admin cannot log into the Django's admin site"
            )
        )

	type = models.PositiveSmallIntegerField(choices=TYPE, default=2)
	
	objects = UserManager()


	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []

	class Meta:
		verbose_name = _('Usuario')
		verbose_name_plural = _('Usuarios')

	def get_full_name(self):
		'''
        Returns the first_name plus the last_name, with a space in between.
        '''
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		'''
        Returns the short name for the user.
        '''
		return self.first_name

	def email_user(self, subject, message, from_email=None, **kwargs):
		'''
		Sends an email to this User.
		'''
		send_mail(subject, message, from_email, [self.email], **kwargs)
