"""add title to requests

Revision ID: e8d7d5a6d724
Revises: 42bdf11f4ef5
Create Date: 2026-06-03 13:33:46.108980

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'e8d7d5a6d724'
down_revision: Union[str, Sequence[str], None] = '42bdf11f4ef5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ✅ ТОЛЬКО добавить колонку title в таблицу requests
    op.add_column('requests', sa.Column('title', sa.String(length=255), nullable=True))

    # 👇 Опционально: заполнить существующие строки
    # op.execute("UPDATE requests SET title = 'Без названия' WHERE title IS NULL")
    # op.alter_column('requests', 'title', nullable=False)


def downgrade() -> None:
    # ✅ Удалить колонку при откате
    op.drop_column('requests', 'title')