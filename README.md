# 🏋️‍♂️ Fitness Studio Booking API

A Django REST API for booking and managing fitness classes like Yoga, Zumba, and HIIT.

---

## 📌 Features

- View available fitness classes
- Book classes with slot validation
- View bookings by client email
- Timezone-aware (IST)
- Input validation and error handling
- Modular, testable codebase
- Logging middleware for request/response tracking

---

## 🛠 Tech Stack

- Python 3.10+
- Django 4+
- Django REST Framework
- SQLite (in-memory or file-based)
- Timezone: `Asia/Kolkata`

---

## 🚀 Setup Instructions

### 🔧 Prerequisites

- Python 3.10+ installed
- Git (optional)

---

### 🧪 Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/amitkumar0198singh/Fitness-Studio.git
cd Fitness-Studio

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Seed sample classes
python manage.py shell
>>> from booking.seeds import run
>>> run()
>>> exit()

# 6. Start the development server
python manage.py runserver
````

---

## 📬 API Endpoints

> Base URL: `http://127.0.0.1:8000/`

---

### ✅ 1. `GET /classes`

Returns a list of upcoming fitness classes.

#### Sample cURL

```bash
curl --location 'http://127.0.0.1:8000/classes/'
```

---

### ✅ 2. `POST /book`

Books a slot for a fitness class.

#### Request Body (JSON)

```json
{
  "client_name": "Amit Kumar",
  "client_email": "amit@example.com",
  "class_id": 1,
  "slots": 2
}
```

#### Sample cURL

```bash
curl --location 'http://127.0.0.1:8000/book/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "client_name": "Amit Kumar Singh",
    "client_email": "amit@singh.com",
    "class_id": 3,
    "slots": 1
}'
```

---

### ✅ 3. `GET /bookings/?email=<email>`

Get all bookings made by a specific email.

#### Sample cURL

```bash
curl --location 'http://127.0.0.1:8000/bookings/?email=amit@singh.com'
```

---

## 🧪 Sample Seed Data

You can modify the seed file at `booking/seeds.py`. Example seed:

```python
[
  {"name": "Yoga", "instructor": "Priya Sharma", "class_time": "..."},
  {"name": "Zumba", "instructor": "Rahul Verma", "class_time": "..."},
  {"name": "HIIT", "instructor": "Anjali Patel", "class_time": "..."}
]
```

Run with:

```python
from booking.seeds import run
run()
exit()
```

---

## 🧼 Code Structure

```bash
booking/
├── views.py              # API logic
├── models.py             # FitnessClass & Booking models
├── serializers.py        # DRF serializers
├── services.py           # Business logic
├── validators.py         # Input validation
├── utils.py              # Utility functions
├── tests.py              # Unit Test
├── seeds.py              # Sample seed data
├── urls.py               # Endpoint routes
├── middlewares.py        # Logging middleware
├── custom_exception.py   # Custom exception classes
├── exceptionhandler.py   # Global DRF exception handler
```


### 📦 Global Exception Handler

Located in `exceptionhandler.py` and configured via:

```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'booking.exceptionhandler.custom_exception_handler',
}
```

---

## 🧪 Logging

All requests and responses are logged via custom middleware (`LogRequestMiddleware`) for debugging.

---

Middleware setup in `settings.py`:

```python
MIDDLEWARE = [
    ...
    'booking.middlewares.LogRequestMiddleware',
]
```

Helps with debugging during development.

---

## 🧪 Logging Sample

Example log output in terminal:

```
========================= Request Data =========================
Request path : /book
Request method : POST
Request content type : application/json
Request user : AnonymousUser
Request IP : 127.0.0.1
Request body : {'client_name': 'Amit', 'client_email': 'amit@example.com', 'class_id': 1}

========================= Response Data =========================
Response status : 200
Response body : {'status': True, 'message': 'Fitness class is booked', ...}
```




## 📹 Loom Video (Walkthrough)

👉 [Click to Watch the Demo](https://www.loom.com/share/115d889b63ce4d8aacbf5f5503bfb0f8?sid=88278496-3f0a-4abe-a2c4-08e5dd1d92a7)

---

## 🙌 Author

**Amit Kumar Singh**
🔗 [GitHub: amitkumar0198singh](https://github.com/amitkumar0198singh)

---

## 📄 License

This project is open-source and free to use.