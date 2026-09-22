"""create books table

Revision ID: 6d27021d7129
Revises: 
Create Date: 2026-09-22 09:39:01.414700

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d27021d7129'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "book",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("pages", sa.Integer(), nullable=False),
        sa.Column("is_available", sa.Boolean(), nullable=False, default=True),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index("ix_book_title", "book", ["title"])
    op.create_index("ix_book_id", "book", ["id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_book_id")
    op.drop_index("ix_book_title")
    op.drop_table("book")
