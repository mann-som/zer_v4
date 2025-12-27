from django.db import models
import uuid
from django.contrib.auth.models import(
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is Required")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, *extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)            

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_code = models.CharField(max_length=20, unique=True, db_index=True)

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15, unique=True)

    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_kyc_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_mobile_verified = models.BooleanField(default=False)
    delete_status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["mobile", "full_name"]


