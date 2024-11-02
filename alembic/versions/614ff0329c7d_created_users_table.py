"""Created Users table

Revision ID: 614ff0329c7d
Revises: 33b857ba8c3d
Create Date: 2024-11-02 08:10:49.677020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '614ff0329c7d'
down_revision: Union[str, None] = '33b857ba8c3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key= True), 
                    sa.Column('email', sa.String(), nullable=False), 
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
