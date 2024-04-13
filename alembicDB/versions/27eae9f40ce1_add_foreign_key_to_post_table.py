"""add foreign-key to post table

Revision ID: 27eae9f40ce1
Revises: 94fb8a9826fd
Create Date: 2024-04-10 18:39:55.864601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27eae9f40ce1'
down_revision: Union[str, None] = '94fb8a9826fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
