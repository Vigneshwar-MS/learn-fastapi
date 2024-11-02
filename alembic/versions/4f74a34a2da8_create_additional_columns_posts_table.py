"""Create additional columns and set foreign key of posts table

Revision ID: 4f74a34a2da8
Revises: 614ff0329c7d
Create Date: 2024-11-02 08:29:02.834546

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f74a34a2da8'
down_revision: Union[str, None] = '614ff0329c7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('ott_release', sa.Boolean(), server_default=sa.text('True'), nullable=False))
    op.add_column('posts', sa.Column('rating', sa.Integer()))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False)),
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False)),
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    
    pass
    


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'rating')
    op.drop_column('posts', 'ott_release')
    pass
