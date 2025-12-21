from django.db import transaction
from .models import User

def generate_user_code():
    with transaction.atomic():
        lastUser = (
            User.objects.select_for_update().order_by("-created_at").first()
        )
        
        if not lastUser or not lastUser.user_code:
            return 'USR000001'
        
        lastNum = int(lastUser.user_code.replace('USR', ''))
        return f"USR{lastNum+1:08d}"