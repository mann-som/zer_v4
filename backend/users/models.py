from django.db import models
import uuid

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    user_code = models.CharField(max_length=20, unique=True, db_index=True)
    
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_kyc_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_mobile_verified = models.BooleanField(default=False)
    delete_status = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    mobile = models.CharField(max_length=15, unique=True)


    def __str__(self):
        return self.email

