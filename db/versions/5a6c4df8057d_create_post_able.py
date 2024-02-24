"""create post able

Revision ID: 5a6c4df8057d
Revises: 
Create Date: 2024-02-24 18:22:00.445280

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a6c4df8057d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.column('id', sa.Integer(), primary_key=True))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
