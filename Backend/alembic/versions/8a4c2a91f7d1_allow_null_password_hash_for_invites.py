"""allow null password hash for invited users

Revision ID: 8a4c2a91f7d1
Revises: 7d1f8c9b12ab
Create Date: 2026-06-02 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a4c2a91f7d1'
down_revision: Union[str, Sequence[str], None] = '7d1f8c9b12ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'users',
        'password_hash',
        existing_type=sa.String(),
        nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'users',
        'password_hash',
        existing_type=sa.String(),
        nullable=False,
    )