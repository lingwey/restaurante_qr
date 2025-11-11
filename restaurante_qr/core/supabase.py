from supabase import create_client
import uuid
from django.conf import settings
import re
import unicodedata

# Inicializar cliente Supabase
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_API_KEY)

def subir_imagen_a_supabase(file, carpeta='generales', bucket=None):

    try:
        bucket = bucket or settings.SUPABASE_BUCKET
        #capta los archivos con caracteres especiales y los normaliza
        nombre_base = unicodedata.normalize('NFKD', file.name).encode('ascii', 'ignore').decode('ascii')
        nombre_base = re.sub(r'[^\w\s\.-]', '', nombre_base).strip().lower()
        nombre_base = re.sub(r'[-\s]+', '_', nombre_base)
        print(f"nombre normalizado:{nombre_base}")
        #toma el nombre base normalizado y lo une con uuid para su subida
        nombre_archivo = f"{carpeta}/{uuid.uuid4().hex}_{nombre_base}"
        #debugging de contro de errores
        print("📤 Subiendo a Supabase...")
        print("🧪 Bucket:", bucket)
        print("🧪 Carpeta:", carpeta)
        print("🧪 Nombre archivo:", file.name)
        print("🧪 Tipo MIME:", file.content_type)
        print("🧪 Tamaño:", file.size)
        
        file_bytes = file.read()
        print("📄 Bytes leídos:", len(file_bytes))
        
        supabase.storage.from_(bucket).upload(
            path=nombre_archivo,
            file=file_bytes, 
            file_options={"content-type": file.content_type}
        )

        
        print(f"🧪 Subiendo a bucket: {bucket}")
        print(f"🧪 Ruta completa: {nombre_archivo}")
        
        print(f"✅ Subida exitosa. Construyendo URL...")
        
        # 2. CONSTRUYE Y DEVUELVE la URL Pública
        url_publica = f"{settings.SUPABASE_URL}/storage/v1/object/public/{bucket}/{nombre_archivo}"
        print(f"🧪 Ruta completa guardada: {url_publica}")

        #return f"{settings.SUPABASE_URL}/storage/v1/object/public/{bucket}/{nombre_archivo}"
        return url_publica

    except Exception as e:
        print(f"Excepción al subir imagen: {e}")
        return None