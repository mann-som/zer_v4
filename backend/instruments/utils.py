from django.db import transaction
from .models import Instrument

def generate_inst_code():
    with transaction.atomic():
        lastInst = (
            Instrument.objects.select_for_update().order_by("-created_at").first()
        )
        
        if not lastInst or not lastInst.instrument_code:
            return 'INST00001'
        
        lastNum = int(lastInst.instrument_code.replace('INST', ''))
        return f"INST{lastNum+1:07d}"