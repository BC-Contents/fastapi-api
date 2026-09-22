"""fix error with author

Revision ID: a8ff7600e682
Revises: c2a4ca782d46
Create Date: 2026-09-22 11:15:55.343349

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8ff7600e682'
down_revision: Union[str, Sequence[str], None] = 'c2a4ca782d46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
