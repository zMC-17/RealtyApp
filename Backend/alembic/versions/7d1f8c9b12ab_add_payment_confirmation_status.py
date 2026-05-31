"""add payment confirmation status and proof fields

Revision ID: 7d1f8c9b12ab
Revises: e114eb3226cb
Create Date: 2026-05-31 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d1f8c9b12ab'
down_revision: Union[str, Sequence[str], None] = 'e114eb3226cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('payments', sa.Column('payment_proof_url', sa.Text(), nullable=True))
    op.add_column('payments', sa.Column('confirmation_requested_at', sa.TIMESTAMP(timezone=True), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('payments', 'confirmation_requested_at')
    op.drop_column('payments', 'payment_proof_url')
