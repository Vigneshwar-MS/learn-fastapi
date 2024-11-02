"""Create posts table with Id, title, genre

Revision ID: 33b857ba8c3d
Revises: 
Create Date: 2024-11-02 07:49:03.466600

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33b857ba8c3d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key= True), 
                    sa.Column('title', sa.String(), nullable=False), 
                    sa.Column('genre', sa.String(), nullable=False)
                    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
