# 🛠 Service Booking API

Ushbu loyiha **xizmat buyurtmalarini boshqarish** va **real-time xabarnomalar** yuborish uchun yaratilgan. Loyihada `client`, `worker` va `admin` rollari mavjud.

---

## ⚙️ Texnologiyalar

* **Backend:** Django, Django REST Framework
* **Auth:** JWT (SimpleJWT)
* **WebSockets:** Django Channels + Redis
* **Database:** PostgreSQL
* **Broker:** Redis

---

## 📌 .env konfiguratsiyasi

Loyihani ishga tushirishdan oldin `backend/.env` fayl yarating:

```env
DEBUG=
SECRET_KEY=

# Database
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

---

## 🚀 O‘rnatish va ishga tushirish

```bash
git clone https://github.com/<username>/<repo>.git
cd <repo>/backend

# Virtual env yaratish
python -m venv env
source env/bin/activate   # Linux/Mac
env\Scripts\activate      # Windows

# Kutubxonalarni o‘rnatish
pip install -r requirements.txt

# Migratsiya
python manage.py migrate

# Superuser yaratish
python manage.py createsuperuser

# Redis ishga tushirish (alohida terminalda)
redis-server

# Serverni ishga tushirish
python manage.py runserver
```

---

## 👤 Autentifikatsiya va Role’lar

* **Registratsiya**: `/api/auth/register/` → foydalanuvchi default **client** sifatida yaratiladi.
* **Login**: `/api/auth/login/` → foydalanuvchiga **JWT token** qaytariladi.
* **Role’lar**:

  * `client` – oddiy foydalanuvchi (default)
  * `worker` – xizmat ko‘rsatuvchi ishchi (admin orqali yaratiladi)
  * `admin` – admin panel orqali boshqaruv

Token orqali barcha API’lar avtorizatsiya qilinadi.

---

## 📦 Order jarayoni

1️⃣ Client buyurtma yaratadi:

```http
POST /api/orders/
Authorization: Bearer <token>
```

👉 Natijada client o‘z WebSocket’ida buyurtma haqida xabar oladi:

```bash
wscat -c "ws://127.0.0.1:8000/ws/orders/client/?client_id=4"
```

Javob:

```json
{
  "message": "Your order 7 was created!",
  "order_id": 7,
  "status": "pending"
}
```

---

2️⃣ Worker buyurtmani o‘ziga oladi:

```http
POST /api/orders/accept/
Authorization: Bearer <worker_token>
```

👉 Worker WebSocket’dan xabar oladi:

```bash
wscat -c "ws://127.0.0.1:8000/ws/orders/workers/"
```

Javob:

```json
{
  "message": "Order 7 was accepted by worker",
  "order_id": 7,
  "status": "in_progress"
}
```

---

## 💳 Payment (Fake)

* **Success**:

  ```http
  POST /api/payments/success/
  ```

  👉 `order.status = paid`

* **Fail**:

  ```http
  POST /api/payments/fail/
  ```

  👉 `order.status = canceled`

Xabar orqali to‘lov natijasi qaytadi (success yoki fail).

---

## 📖 Order History

* **Client** → faqat o‘z buyurtmalarini ko‘radi
* **Worker** → o‘z mutaxassisligiga tegishli buyurtmalarni ko‘radi
* **Admin** → barcha buyurtmalarni ko‘ra oladi

---

## 📜 Swagger

Barcha endpointlarni Swagger’dan test qilishingiz mumkin:

👉 [http://127.0.0.1:8000/api/swagger/](http://127.0.0.1:8000/api/swagger/)
