"""add content column

Revision ID: 48172f5ad780
Revises: 5a6c4df8057d
Create Date: 2024-02-24 18:36:25.159351

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48172f5ad780'
down_revision: Union[str, None] = '5a6c4df8057d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
