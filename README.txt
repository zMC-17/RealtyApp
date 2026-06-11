# Realty App — Система управления недвижимостью и арендой

## 📋 Описание
Full-stack приложение для управления недвижимостью и договорами аренды.
- **Backend**: FastAPI + SQLAlchemy 2.0 (async) + PostgreSQL
- **Frontend**: Vue 3 + TypeScript + Vite

## 🏗️ Архитектура

```
RealtyApp/
├─ Backend/
│  ├─ app/
│  │  ├─ core/           (конфигурация, БД, безопасность)
│  │  ├─ models/         (ORM модели)
│  │  ├─ schemas/        (Pydantic валидация)
│  │  ├─ services/       (бизнес-логика)
│  │  ├─ routers/        (API эндпоинты)
│  │  └─ main.py         (FastAPI приложение)
│  ├─ alembic/           (миграции БД)
│  └─ requirements.txt   (зависимости)
│
├─ Frontend/
│  ├─ src/
│  │  ├─ components/
│  │  ├─ pages/
│  │  ├─ router/
│  │  ├─ services/
│  │  ├─ stores/
│  │  └─ main.ts
│  └─ package.json
│
└─ documentation/        (документация)
```
