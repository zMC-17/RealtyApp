## Database Schema - Диаграмма

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DATABASE RELATIONSHIPS                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌──────────────────────┐
│      USERS           │
├──────────────────────┤
│ id (PK)              │
│ name                 │◄─────────────────────────┐
│ email (UNIQUE)       │                          │
│ password_hash        │                          │
│ created_at           │                          │
│ updated_at           │                          │
└──────────────────────┘                          │
       │                                           │
       │                                           │
       │ owner_id (1 to many)                      │
       │                                           │
       ▼                                           │
┌──────────────────────┐              ┌───────────┴──────────────┐
│   PROPERTIES         │              │                          │
├──────────────────────┤              │                          │
│ id (PK)              │              │                          │
│ owner_id (FK→users)  │◄─────────────┘                          │
│ title                │                                         │
│ address              │              ┌──────────────────────┐   │
│ description          │              │   CONTRACTS          │   │
│ property_type        │              ├──────────────────────┤   │
│ created_at           │              │ id (PK)              │   │
│ updated_at           │              │ property_id (FK)─────┼───┘
└──────────────────────┘              │ tenant_id (FK)───────┼───┐
       │                              │ start_date           │   │
       │                              │ end_date             │   │
       │ property_id (1 to many)      │ status               │   │
       │                              │ monthly_payment      │   │
       │                              │ created_at           │   │
       │                              │ updated_at           │   │
       ▼                              └──────────────────────┘   │
┌──────────────────────┐                     │ contract_id       │
│   REQUESTS           │                     │ (1 to many)       │
├──────────────────────┤                     │                   │
│ id (PK)              │              ┌──────┴────────┬──────────┘
│ contract_id (FK)─────┼──────┐       │               │
│ property_id (FK)─────┼──────┼────┐  │               │
│ message              │      │    │  │               │
│ status               │      │    │  │               │
│ request_date         │      │    │  │               │
│ created_at           │      │    │  │               │
│ updated_at           │      │    │  │               │
└──────────────────────┘      │    │  │               │
                              │    │  │               │
┌──────────────────────┐      │    │  │               │
│   PAYMENTS           │      │    │  │               │
├──────────────────────┤      │    │  │               │
│ id (PK)              │      │    │  │               │
│ contract_id (FK)─────┼──────┘    │  │               │
│ amount               │           │  │               │
│ due_date             │           │  │               │
│ paid_at              │           │  │               │
│ status               │           │  │               │
│ comment              │           │  │               │
│ created_at           │           │  │               │
│ updated_at           │           │  │               │
└──────────────────────┘           │  │               │
                                   │  └───────────────┘
                                   └──────────── (1:many)
                                        Contracts
                                   have Requests & Payments
```

---

### 📊 Подробная таблица связей

| Таблица | Поле | Тип | Связь | Комментарий |
|---------|------|-----|-------|------------|
| **users** | id | INT PK | - | Пользователь (арендодатель или арендатор) |
| | email | STRING | UNIQUE, INDEX | Электронная почта уникальна |
| | password_hash | STRING | - | Хэш пароля для безопасности |
| **properties** | owner_id | INT FK | → users.id | Собственник объекта |
| | address | STRING | INDEX | Адрес для быстрого поиска |
| **contracts** | property_id | INT FK | → properties.id | Договор на конкретный объект |
| | tenant_id | INT FK | → users.id | Арендатор (пользователь) |
| **requests** | contract_id | INT FK | → contracts.id | Заявка по договору |
| | property_id | INT FK | → properties.id | Заявка на конкретный объект |
| **payments** | contract_id | INT FK | → contracts.id | Платёж по договору |

---

### 🔄 Жизненный цикл записей

```
1. User регистрируется
   ↓
   users [id=1, name="Иван", email="ivan@mail.com"]

2. User создаёт Property
   ↓
   properties [id=1, owner_id=1, title="Квартира", address="Москва"]

3. Создаётся Contract между User (как tenant) и Property (owner=другой User)
   ↓
   contracts [id=1, property_id=1, tenant_id=2, start_date="2026-06-01", ...]

4. Tenant подаёт Request по обслуживанию
   ↓
   requests [id=1, contract_id=1, message="Сломалась дверь", status="новая"]

5. Создаются Payment записи для каждого платежа по Contract
   ↓
   payments [id=1, contract_id=1, amount=50000, due_date="2026-07-01", status="ожидается"]
            [id=2, contract_id=1, amount=50000, due_date="2026-08-01", status="оплачено"]
```

---

### 📋 Правила целостности

```sql
-- users
ALTER TABLE users ADD CONSTRAINT uq_email UNIQUE(email);
CREATE INDEX idx_email ON users(email);

-- properties
ALTER TABLE properties ADD CONSTRAINT fk_owner FOREIGN KEY (owner_id) REFERENCES users(id);
CREATE INDEX idx_owner ON properties(owner_id);

-- contracts  
ALTER TABLE contracts ADD CONSTRAINT fk_property FOREIGN KEY (property_id) REFERENCES properties(id);
ALTER TABLE contracts ADD CONSTRAINT fk_tenant FOREIGN KEY (tenant_id) REFERENCES users(id);
CREATE INDEX idx_property ON contracts(property_id);
CREATE INDEX idx_tenant ON contracts(tenant_id);

-- requests
ALTER TABLE requests ADD CONSTRAINT fk_contract FOREIGN KEY (contract_id) REFERENCES contracts(id);
ALTER TABLE requests ADD CONSTRAINT fk_property FOREIGN KEY (property_id) REFERENCES properties(id);
CREATE INDEX idx_contract ON requests(contract_id);
CREATE INDEX idx_property_req ON requests(property_id);

-- payments
ALTER TABLE payments ADD CONSTRAINT fk_contract_payment FOREIGN KEY (contract_id) REFERENCES contracts(id);
CREATE INDEX idx_contract_pay ON payments(contract_id);
```

---

### 🔍 Примеры запросов

```python
# Получить все объекты пользователя
user = await session.get(User, user_id)
properties = user.properties  # ✅ Работает благодаря relationship

# Получить все договоры по объекту
property_obj = await session.get(Properties, property_id)
contracts = property_obj.contracts  # ✅ Двусторонняя связь

# Получить все платежи по договору
contract = await session.get(Contract, contract_id)
payments = contract.payments  # ✅ Через relationship

# Фильтр по заявкам с определённым статусом
from sqlalchemy import select
stmt = select(Request).where(Request.status == 'новая')
requests = await session.execute(stmt)
```

---

**Дата:** 26 мая 2026
