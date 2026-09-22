"""make book pages optional

Revision ID: d4f2c8a9b1e0
Revises: 9ba96e651b3f
Create Date: 2026-09-22

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d4f2c8a9b1e0"
down_revision: Union[str, Sequence[str], None] = "cf0f74d0ff4e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Allow books without a page count."""
    with op.batch_alter_table("book") as batch_op:
        batch_op.alter_column(
            "pages",
            existing_type=sa.Integer(),
            nullable=True,
        )


def downgrade() -> None:
    """Restore the required page count constraint."""
    with op.batch_alter_table("book") as batch_op:
        batch_op.alter_column(
            "pages",
            existing_type=sa.Integer(),
            nullable=False,
        )
