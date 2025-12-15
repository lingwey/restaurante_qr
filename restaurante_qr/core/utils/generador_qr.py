import qrcode
from io import BytesIO
from django.core.files import File
from django.conf import settings

def generar_qr_para_mesa(mesa):
    # URL base configurable desde settings.py
    base_url = getattr(settings, "QR_BASE_URL", "http://localhost:8000")
    
    # URL que se codifica en el QR
    url = f"{base_url}/menu?restaurante={mesa.restaurante.id}&mesa={mesa.id}"
    
    # Generación del QR
    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer)
    
    # Guardado en el modelo Mesa
    filename = f"mesa_{mesa.numero}_qr.png"
    mesa.qr_code.save(filename, File(buffer), save=True)
