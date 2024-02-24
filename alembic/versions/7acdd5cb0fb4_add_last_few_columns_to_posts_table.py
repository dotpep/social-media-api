"""add last few columns to posts table

Revision ID: 7acdd5cb0fb4
Revises: cc1c96ff506a
Create Date: 2024-02-24 17:22:58.002265

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7acdd5cb0fb4'
down_revision: Union[str, None] = 'cc1c96ff506a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('published', sa.Boolean, server_default='TRUE', nullable=False)
    )
    op.add_column(
        'posts',
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                  server_default=sa.text('NOW()'), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
