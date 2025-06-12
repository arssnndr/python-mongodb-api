# Python MongoDB REST API

Aplikasi backend REST API CRUD menggunakan Python (FastAPI) dan MongoDB dengan Docker.

## Fitur

- ✅ CRUD Operations (Create, Read, Update, Delete)
- ✅ MongoDB sebagai database
- ✅ FastAPI sebagai web framework
- ✅ Docker untuk containerization MongoDB
- ✅ Pydantic untuk data validation
- ✅ Error handling
- ✅ Dokumentasi API otomatis (Swagger UI)
- ✅ Pagination untuk GET requests
- ✅ Unique email validation

## Teknologi yang Digunakan

- **Python 3.8+**
- **FastAPI** - Modern web framework untuk API
- **MongoDB** - NoSQL database
- **PyMongo** - MongoDB driver untuk Python
- **Pydantic** - Data validation
- **Docker & Docker Compose** - Containerization
- **Uvicorn** - ASGI server

## Struktur Project

```
python-mongodb-api/
├── main.py              # FastAPI application dengan routes
├── database.py          # Database connection dan konfigurasi
├── models.py            # Pydantic models untuk validasi data
├── requirements.txt     # Python dependencies
├── docker-compose.yml   # Docker setup untuk MongoDB
├── .env                 # Environment variables
└── README.md           # Dokumentasi
```

## Setup dan Instalasi

### 1. Clone atau Download Project

```bash
git clone https://github.com/arssnndr/python-mongodb-api.git
cd python-mongodb-api
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start MongoDB dengan Docker

```bash
docker-compose up -d
```

Ini akan menjalankan:
- MongoDB pada port 27017
- Mongo Express (Web UI) pada port 8081

### 4. Jalankan Aplikasi

```bash
python main.py
```

Atau menggunakan uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### Base URL: `http://localhost:8000`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| POST | `/users` | Create new user |
| GET | `/users` | Get all users (with pagination) |
| GET | `/users/{user_id}` | Get user by ID |
| PUT | `/users/{user_id}` | Update user by ID |
| DELETE | `/users/{user_id}` | Delete user by ID |
| GET | `/users/count` | Get total users count |

### User Model

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "age": 30,
  "city": "Jakarta"
}
```

## Contoh Penggunaan API

### 1. Create User

```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "age": 30,
    "city": "Jakarta"
  }'
```

### 2. Get All Users

```bash
curl -X GET "http://localhost:8000/users"
```

Dengan pagination:

```bash
curl -X GET "http://localhost:8000/users?skip=0&limit=10"
```

### 3. Get User by ID

```bash
curl -X GET "http://localhost:8000/users/{user_id}"
```

### 4. Update User

```bash
curl -X PUT "http://localhost:8000/users/{user_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "age": 25
  }'
```

### 5. Delete User

```bash
curl -X DELETE "http://localhost:8000/users/{user_id}"
```

## Dokumentasi API (Swagger UI)

Setelah aplikasi berjalan, akses dokumentasi interaktif di:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## MongoDB Management

### Mongo Express (Web UI)

Akses Mongo Express di: http://localhost:8081

### MongoDB Connection

```
Host: localhost
Port: 27017
Username: admin
Password: password123
Database: myapp
```

## Environment Variables

File `.env` berisi konfigurasi berikut:

```
MONGODB_URL=mongodb://admin:password123@localhost:27017/myapp?authSource=admin
DATABASE_NAME=myapp
COLLECTION_NAME=users
```

## Error Handling

API mengembalikan error response dengan format:

```json
{
  "detail": "Error message"
}
```

HTTP Status Codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `409` - Conflict (email sudah ada)
- `500` - Internal Server Error
- `503` - Service Unavailable

## Testing

Untuk testing API, gunakan:

1. **Swagger UI** - http://localhost:8000/docs
2. **Postman** - Import collection dari dokumentasi
3. **curl** - Command line testing
4. **Python requests** - Programmatic testing

## Stop Services

```bash
# Stop aplikasi FastAPI
Ctrl+C

# Stop MongoDB Docker containers
docker-compose down
```

## Troubleshooting

### MongoDB Connection Error

1. Pastikan Docker berjalan
2. Cek apakah container MongoDB aktif: `docker ps`
3. Restart containers: `docker-compose restart`

### Port Already in Use

1. Cek process yang menggunakan port: `lsof -i :8000` atau `lsof -i :27017`
2. Kill process atau gunakan port lain

### Permission Error

1. Pastikan user memiliki permission untuk Docker
2. Jalankan dengan sudo jika diperlukan (tidak disarankan)

## Pengembangan Lanjutan

Untuk pengembangan lebih lanjut:

1. **Authentication & Authorization** (JWT)
2. **Rate Limiting**
3. **Caching** (Redis)
4. **Logging**
5. **Unit Tests**
6. **API Versioning**
7. **File Upload**
8. **Search & Filtering**
9. **Data Export** (CSV, PDF)
10. **Background Tasks** (Celery)

