import asyncio
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

# путь до приложения
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
from app.core.database import Base

# Alembic Config
config = context.config

# Логирование
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные для автогенерации
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Миграции в 'offline' режиме.

    Используется по умолчанию при autogenerate.
    Работает с async БД без greenlet.
    """
    url = config.get_main_option("sqlalchemy.url", settings.DATABASE_URL)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Выполнить миграции через синхронное подключение."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Миграции в 'online' режиме (требует greenlet).

    Используется для реального применения миграций к БД.
    """
    connectable = create_async_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async with connectable.begin() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


# По умолчанию используется offline режим для autogenerate
# Для apply миграций используйте: alembic upgrade head
if context.is_offline_mode():
    run_migrations_offline()
else:
    # Для online режима потребуется установить greenlet
    try:
        asyncio.run(run_migrations_online())
    except ValueError as e:
        if "greenlet" in str(e):
            print("\n⚠️  Для online режима нужна greenlet:")
            print("   pip install greenlet")
            print("\nАльтернатива: используйте offline режим (по умолчанию)")
        raise
