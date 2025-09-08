import qrcode
from io import BytesIO
from django.core.files import File

def generar_qr_para_mesa(mesa):
    url = f"https://tusitio.com/pedido/mesa/{mesa.identificador_qr}/"
    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer)
    return File(buffer, name=f"mesa_{mesa.numero}_qr.png")
