"""Init

Revision ID: a1cd5a86bf0d
Revises: 
Create Date: 2026-09-09 21:19:37.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'a1cd5a86bf0d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'page',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_page_id'), 'page', ['id'], unique=False)
    op.create_index(op.f('ix_page_name'), 'page', ['name'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_page_name'), table_name='page')
    op.drop_index(op.f('ix_page_id'), table_name='page')
    op.drop_table('page')
