"""add authors table and author_id to books

Revision ID: 0a83a52985a0
Revises: 6d27021d7129
Create Date: 2026-09-22 10:04:34.289428

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a83a52985a0'
down_revision: Union[str, Sequence[str], None] = '6d27021d7129'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("biography", sa.String(length=500), nullable=True),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index("ix_authors_name", "authors", ["name"])
    op.create_index("ix_authors_id", "authors", ["id"])
    op.add_column("book", sa.Column("author_id", sa.Integer(), nullable=True))
    op.create_foreign_key("fk_book_author_id", "book", "authors", ["author_id"], ["id"], ondelete="SET NULL")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_book_author_id", "book", type_="foreignkey")
    op.drop_column("book", "author_id")
    op.drop_index("ix_authors_id")
    op.drop_index("ix_authors_name")
    op.drop_table("authors")
