# 🚀 Quick Start Guide

## Langkah-langkah Menjalankan Aplikasi

### 1. Pastikan Docker berjalan
```bash
sudo systemctl start docker
# atau
docker ps
```

### 2. Jalankan MongoDB dengan Docker
```bash
docker compose up -d
```

### 3. Install Dependencies Python
```bash
pip install -r requirements.txt
```

### 4. Jalankan API Server
```bash
python main.py
```

### 5. Test API (buka terminal baru)
```bash
python test_api.py
```

## ⚡ Cara Cepat

Jalankan satu command:
```bash
python run.py
```

## 🌐 Akses Aplikasi

- **API Server**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **MongoDB UI (Mongo Express)**: http://localhost:8081

## 🛑 Stop Aplikasi

1. Stop API server: `Ctrl+C`
2. Stop MongoDB: `docker compose down`

## 🧪 Test Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Get all users
curl http://localhost:8000/users

# Create user
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@test.com","age":30}'
```

