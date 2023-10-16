"""create tables

Revision ID: ad471e9577d4
Revises: 5a1aee97c768
Create Date: 2023-10-16 22:59:04.074642

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad471e9577d4'
down_revision: Union[str, None] = '5a1aee97c768'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('username', sa.String(length=25), nullable=False),
        sa.Column('password', sa.String(128), nullable=False)
    )

    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('content', sa.String(512), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('sender_id', sa.Integer(), nullable=False),
        sa.Column('recipient_id', sa.Integer(), nullable=False)
    )


def downgrade():
    op.drop_table('messages')
    op.drop_table('users')
