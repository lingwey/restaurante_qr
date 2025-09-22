# Restaurante QR

Sistema de gestión de pedidos para restaurantes mediante escaneo de códigos QR. Diseñado con Django y Channels para comunicación en tiempo real, y pensado para escalar fácilmente en entornos dockerizados y con integración futura a Supabase.

---

## Objetivos del proyecto

- Digitalizar el proceso de pedidos en restaurantes.
- Permitir a los clientes escanear un QR en su mesa y realizar pedidos desde su dispositivo.
- Ofrecer a los mozos y cocina una vista en tiempo real del estado de cada pedido.
- Facilitar la administración del menú, mesas y horarios desde un panel intuitivo.

---

## Arquitectura modular

El proyecto está dividido en apps independientes para mantener la escalabilidad y claridad del código:

| App           | Rol principal |
|---------------|----------------|
| `restaurantes` | Gestión de restaurantes y mesas |
| `menu`         | Administración de platos y categorías |
| `pedidos`      | Flujo de pedidos y estados |
| `clientes`     | Interfaz pública para escaneo QR |
| `usuarios`     | Autenticación y roles |
| `core`         | Utilidades compartidas, modelos base, generación de QR |

---

## Tecnologías utilizadas

- Django 5.1.4
- Django Channels + Daphne
- Redis
- Pillow + qrcode
- Python-dotenv
## aun no implementados 
- Docker (próximamente) 
- Supabase (en exploración)
- PostgreSQL
---

## Instalación rápida

```bash
# Clonar el repositorio
git clone https://github.com/lingwey/restaurante_qr.git
cd restaurante_qr

# Crear entorno virtual
python -m venv mi_entorno
source mi_entorno/bin/activate  # o mi_entorno\Scripts\activate en Windows

# Instalar dependencias
pip install -r requirements.txt

# Migraciones iniciales
python manage.py migrate

# Ejecutar el servidor
python manage.py runserver
