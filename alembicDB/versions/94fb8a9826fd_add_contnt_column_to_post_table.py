"""add contnt column to post table

Revision ID: 94fb8a9826fd
Revises: 26dd25bcfc29
Create Date: 2024-04-10 18:24:04.943891

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94fb8a9826fd'
down_revision: Union[str, None] = '26dd25bcfc29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
