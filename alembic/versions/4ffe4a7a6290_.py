"""empty message

Revision ID: 4ffe4a7a6290
Revises: 8afebb7d4dd1
Create Date: 2023-11-25 11:38:00.997001

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ffe4a7a6290'
down_revision: Union[str, None] = '8afebb7d4dd1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
