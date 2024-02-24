"""add centent column to posts table

Revision ID: 92a2dfb28c35
Revises: 79e04655029c
Create Date: 2024-02-24 17:03:59.199489

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92a2dfb28c35'
down_revision: Union[str, None] = '79e04655029c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('content', sa.String, nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
