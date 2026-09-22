"""fix error with author in book model

Revision ID: 9ba96e651b3f
Revises: a8ff7600e682
Create Date: 2026-09-22 11:17:44.939484

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ba96e651b3f'
down_revision: Union[str, Sequence[str], None] = 'a8ff7600e682'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
