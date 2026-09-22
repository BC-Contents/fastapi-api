"""add authors table and author_id to books and fix

Revision ID: c2a4ca782d46
Revises: 0a83a52985a0
Create Date: 2026-09-22 10:58:49.816243

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2a4ca782d46'
down_revision: Union[str, Sequence[str], None] = '0a83a52985a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
