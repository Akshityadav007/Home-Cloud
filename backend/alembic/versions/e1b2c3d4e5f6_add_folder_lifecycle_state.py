"""add folder lifecycle state

Revision ID: e1b2c3d4e5f6
Revises: dfc82d7977f4
Create Date: 2026-07-12 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'dfc82d7977f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'folders',
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        'folders',
        sa.Column(
            'is_permanent_delete',
            sa.Boolean(),
            nullable=False,
            server_default='false'
        )
    )


def downgrade() -> None:
    op.drop_column('folders', 'is_permanent_delete')
    op.drop_column('folders', 'deleted_at')
