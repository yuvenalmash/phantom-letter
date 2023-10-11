"""inital migration 2

Revision ID: d4ebdeed0665
Revises: f5fc7d470a26
Create Date: 2023-10-11 23:28:43.424316

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4ebdeed0665'
down_revision: Union[str, None] = 'f5fc7d470a26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
