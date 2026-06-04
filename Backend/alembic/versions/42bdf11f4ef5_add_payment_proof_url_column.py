"""add payment_proof_url column

Revision ID: 42bdf11f4ef5
Revises: 8a4c2a91f7d1
Create Date: 2024-01-01 12:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "42bdf11f4ef5"
down_revision = "8a4c2a91f7d1"
branch_labels = None
depends_on = None


def upgrade():
    # ✅ ТОЛЬКО добавить колонку
    op.add_column(
        "payments", sa.Column("payment_proof_url", sa.String(), nullable=True)
    )


def downgrade():
    # ✅ ТОЛЬКО удалить колонку (если нужен откат)
    op.drop_column("payments", "payment_proof_url")
