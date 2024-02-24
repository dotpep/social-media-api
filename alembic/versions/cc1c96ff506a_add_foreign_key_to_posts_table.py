"""add foreign key to posts table

Revision ID: cc1c96ff506a
Revises: 5df57a9f2976
Create Date: 2024-02-24 17:17:06.329409

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc1c96ff506a'
down_revision: Union[str, None] = '5df57a9f2976'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('owner_id', sa.Integer, nullable=False)
    )
    op.create_foreign_key(
        'post_users_fkey',
        source_table='posts',
        referent_table='users',
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fkey', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
