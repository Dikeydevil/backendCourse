"""add users

Revision ID: 641dcd726a10
Revises: 35ca8357c129
Create Date: 2025-07-07 22:58:31.728139

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "641dcd726a10"
down_revision: Union[str, None] = "35ca8357c129"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "id",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("password", sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

def downgrade() -> None:
    op.drop_table("id")
