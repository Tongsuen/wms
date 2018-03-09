from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,BaseUserManager
)

# Create your models here.
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,email,password=None,name=None,tel=None,is_active=True,is_staff = False,is_admin=False,is_company=False):
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("User must have a password")

        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.name = name
        user_obj.tel = tel
        user_obj.company = is_company
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self,email,password=None):
        user = self.create_user(email,password=password,is_staff = True)
        return user

    def create_superuser(self,email,password=None):
        user = self.create_user(email,password=password,is_staff = True,is_admin=True)
        return user

class User(AbstractBaseUser):
    email   =   models.EmailField(max_length=255,unique=True)
    name    =   models.CharField(blank=False, max_length=120,null=True)
    tel     = models.CharField(max_length=120,null=True)


    active  =   models.BooleanField(default=True)
    company =   models.BooleanField(default=False)
    staff   =   models.BooleanField(default=True)
    admin   =   models.BooleanField(default=True)

    address_pk  = models.IntegerField(default=0)

    timestamp = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD  = 'email'

    REQUIRED_FIELD = [email]

    objects = UserManager()

    def __str__(self):
        return  self.email

    def get_full_name(self):
        if self.name:
            return self.name
        return  self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm,obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_company(self):
        return  self.company
    @property
    def is_staff(self):
        return  self.staff

    @property
    def is_admin(self):
        return  self.admin

    @property
    def is_active(self):
        return  self.active

class Address(models.Model):
    detail          = models.CharField(blank=False,max_length=255)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active       = models.BooleanField(default=1)

    def __str__(self):
        return  self.detail

class Driver(models.Model):
    name    =   models.CharField(blank=False, max_length=120,null=True)
    tel     = models.CharField(max_length=120,null=True)
    active       = models.BooleanField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  self.name
